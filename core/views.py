from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from core.auth import User
from core.error_messages import ERROR_MESSAGES
from .models import Brand, Product, Cart, Order, CarModel, CarYear, CarSeries
from django.contrib.auth import login, logout, authenticate


def set_language(request, lang):
    request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))

def add_session_message(request, message, msg_type='error'):
    """Helper function to add a message to the session."""
    if 'messages' not in request.session:
        request.session['messages'] = []
    request.session['messages'].append({'message': message, 'type': msg_type})
    request.session.modified = True

def get_error_message(code, request):
    lang = request.session.get('lang', 'uz')
    return ERROR_MESSAGES.get(code, {}).get(lang, 'Xatolik!')

def home(request):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    brands = Brand.objects.all()
    ctx = {'brands': brands, 'lang': lang}
    if 'messages' in request.session:
        ctx['messages'] = request.session.pop('messages')
    return render(request, 'pages/index.html', ctx)

def products(request):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    search = request.GET.get('search', '').strip()
    brand_ids = [id for id in request.GET.getlist('brand_ids') if id]
    model_ids = [id for id in request.GET.getlist('model_ids') if id]
    year_ids = [id for id in request.GET.getlist('year_ids') if id]
    series_ids = [id for id in request.GET.getlist('series_ids') if id]

    products = Product.objects.filter(deleted=False).prefetch_related('images')

    if search:
        products = products.filter(
            Q(name_ru__icontains=search) |
            Q(name_uz__icontains=search) |
            Q(name_en__icontains=search) |
            Q(name_ger__icontains=search) |
            Q(brand__name__icontains=search)
        )

    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)
    if model_ids:
        products = products.filter(car_model_id__in=model_ids)
    if year_ids:
        products = products.filter(car_year_id__in=year_ids)
    if series_ids:
        products = products.filter(car_series_id__in=series_ids)

    products = products.distinct()

    brands = Brand.objects.all()
    years = CarYear.objects.filter(deleted=False)
    series = CarSeries.objects.filter(deleted=False)

    if model_ids:
        years = years.filter(model_id__in=model_ids).distinct().order_by('year')
    if year_ids:
        series = series.filter(year_id__in=year_ids).distinct()

    ctx = {
        'products': products,
        'lang': lang,
        'brands': brands,
        'years': years,
        'series': series,
        'search': search,
        'selected_brand_ids': brand_ids,
        'selected_model_ids': model_ids,
        'selected_year_ids': year_ids,
        'selected_series_ids': series_ids,
        'filter_active': bool(brand_ids or model_ids)
    }
    if 'messages' in request.session:
        ctx['messages'] = request.session.pop('messages')
    return render(request, 'pages/products.html', ctx)

def productsBrand(request):
    """View to display products filtered by brand"""
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    
    brand_id = request.GET.get('brand_id')
    search = request.GET.get('search', '').strip()
    
    # Get all brands for the filter
    brands = Brand.objects.all()
    
    # Filter products by brand if brand_id is provided
    products = Product.objects.filter(deleted=False).prefetch_related('images')
    
    if brand_id:
        products = products.filter(brand_id=brand_id)
        selected_brand = Brand.objects.filter(id=brand_id).first()
    else:
        selected_brand = None
    
    # Apply search filter if provided
    if search:
        products = products.filter(
            Q(name_ru__icontains=search) |
            Q(name_uz__icontains=search) |
            Q(name_en__icontains=search) |
            Q(name_ger__icontains=search) |
            Q(brand__name__icontains=search)
        )
    
    products = products.distinct()
    
    ctx = {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'lang': lang,
        'search': search,
        'brand_id': brand_id
    }
    
    if 'messages' in request.session:
        ctx['messages'] = request.session.pop('messages')
    
    return render(request, 'pages/productsBrand.html', ctx)

def product_detail(request, pk):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    product_one = Product.objects.prefetch_related('images').filter(pk=pk, deleted=False).first()
    if not product_one:
        add_session_message(request, get_error_message('product_not_found', request), 'error')
        return redirect('products')
    ctx = {'product_one': product_one, 'lang': lang}
    if 'messages' in request.session:
        ctx['messages'] = request.session.pop('messages')
    return render(request, 'pages/productDetails.html', ctx)

def basket(request):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    carts = Cart.objects.filter(user=request.user, status=True) if request.user.is_authenticated else []
    ctx = {'carts': carts, 'lang': lang, 'basket_count': carts.count()}
    if 'messages' in request.session:
        ctx['messages'] = request.session.pop('messages')
    return render(request, 'pages/basket.html', ctx)

def change_cart(request, cart_id, inc):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': get_error_message('not_authenticated', request)})
    cart = Cart.objects.filter(id=cart_id, user=request.user).first()
    if cart:
        if inc:
            cart.quantity += 1
        else:
            cart.quantity = max(1, cart.quantity - 1)
        cart.save()
        return JsonResponse({'success': True, 'total_balance': request.user.calculate_cart()})
    return JsonResponse({'success': False, 'error': 'Cart not found'})

@require_POST
def cart_add(request, add_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not request.user.is_authenticated:
        error_message = get_error_message('not_authenticated', request)
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_message})
        add_session_message(request, error_message, 'error')
        return redirect(request.META.get('HTTP_REFERER', 'products'))

    product = Product.objects.filter(id=add_id, deleted=False).first()
    if not product:
        error_message = get_error_message('product_not_found', request)
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_message})
        add_session_message(request, error_message, 'error')
        return redirect(request.META.get('HTTP_REFERER', 'products'))

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product, status=True)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        success_message = get_error_message('already_in_cart', request)
    else:
        success_message = get_error_message('cart_added', request)

    if is_ajax:
        return JsonResponse({'success': True, 'message': success_message})
    add_session_message(request, success_message, 'success')
    return redirect(request.META.get('HTTP_REFERER', 'products'))

@login_required
def cart_remove(request, remove_id):
    product = Product.objects.filter(id=remove_id, deleted=False).first()
    if product:
        Cart.objects.filter(user=request.user, product=product, status=True).delete()
        add_session_message(request, get_error_message('cart_removed', request), 'success')
    else:
        add_session_message(request, get_error_message('product_not_found', request), 'error')
    return redirect(request.META.get('HTTP_REFERER', 'products'))

@require_POST
def login_view(request):
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    next_url = request.POST.get('next') or '/'
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({'success': True, 'next': next_url})
    return JsonResponse({'success': False, 'error': get_error_message('login_failed', request)})

@require_POST
def register_view(request):
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    name = request.POST.get('username')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    if not all([name, phone, password]):
        return JsonResponse({'success': False, 'error': 'Заполните все поля'})
    if User.objects.filter(phone=phone).exists():
        return JsonResponse({'success': False, 'error': get_error_message('phone_already_exists', request)})
    user = User.objects.create_user(phone=phone, username=name, password=password)
    login(request, user)
    return JsonResponse({'success': True, 'next': '/'})

@login_required
def logout_view(request):
    logout(request)
    add_session_message(request, get_error_message('logout_success', request), 'info')
    return redirect('home')

@login_required
@require_POST
def order_create(request):
    try:
        product_id = request.POST.get('productId')
        quantity = int(request.POST.get('productQuantity', 1))
        full_name = request.POST.get('fullName')
        phone = request.POST.get('contactPhone')
        email = request.POST.get('email')
        additional_info = request.POST.get('additionalInfo')

        if not all([product_id, full_name, phone, email]):
            return JsonResponse({'success': False, 'message': 'Заполните все обязательные поля!'})

        product = Product.objects.get(id=product_id, deleted=False)
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            full_name=full_name,
            phone=phone,
            email=email,
            additional_info=additional_info or ''
        )
        return JsonResponse({'success': True, 'message': get_error_message('order_success', request)})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': get_error_message('product_not_found', request)})
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Неверное количество!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': get_error_message('invalid_request', request)})

@require_GET
def reset_filters(request):
    lang = request.session.get('lang', 'uz')
    return redirect(f'/products/?lang={lang}')

@require_GET
def get_models(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(deleted=False)
    if brand_id:
        models = models.filter(brand_id=brand_id)
    return JsonResponse(list(models.values('id', 'name')), safe=False)

@require_GET
def get_years(request):
    model_id = request.GET.get('model_id')
    years = CarYear.objects.filter(deleted=False).order_by('year')
    if model_id:
        years = years.filter(model_id=model_id)
    return JsonResponse(list(years.values('id', 'year')), safe=False)

@require_GET
def get_series(request):
    year_id = request.GET.get('year_id')
    series = CarSeries.objects.filter(deleted=False)
    if year_id:
        series = series.filter(year_id=year_id)
    return JsonResponse(list(series.values('id', 'name')), safe=False)