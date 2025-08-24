from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from core.auth import User
from core.error_messages import ERROR_MESSAGES
from .models import Brand, Product, Cart, Order, CarModel, CarYear, CarSeries
from django.contrib.auth import login, logout, authenticate


def set_language(request, lang):
    request.session["lang"] = lang
    return redirect(request.META.get("HTTP_REFERER", "/"))

def get_error_message(code, request):
    lang = request.session.get("lang", "uz")
    return ERROR_MESSAGES.get(code, {}).get(lang, "Xatolik!")

def home(request):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    brands = Brand.objects.all()
    return render(request, 'pages/index.html', {"brands": brands, "lang": lang})

def products(request):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    search = request.GET.get("search", "").strip()
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
    car_models = CarModel.objects.filter(deleted=False)  # Renamed to avoid confusion
    years = CarYear.objects.filter(deleted=False)
    series = CarSeries.objects.filter(deleted=False)

    if model_ids:
        years = years.filter(model_id__in=model_ids).distinct().order_by('year')
    if year_ids:
        series = series.filter(year_id__in=year_ids).distinct()

    ctx = {
        "products": products,
        "lang": lang,
        "brands": brands,
        "car_models": car_models,  # Changed from 'models' to 'car_models'
        "years": years,
        "series": series,
        "search": search,
        "selected_brand_ids": brand_ids,
        "selected_model_ids": model_ids,
        "selected_year_ids": year_ids,
        "selected_series_ids": series_ids,
        "error": request.session.pop("error", None),
        "filter_active": bool(brand_ids and model_ids)
    }
    return render(request, 'pages/products.html', ctx)

def product_detail(request, pk):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    product_one = Product.objects.prefetch_related('images').filter(pk=pk).first()
    ctx = {
        "product_one": product_one,
        "lang": lang,
        "error": request.session.pop("error", None)
    }
    return render(request, 'pages/productDetails.html', ctx)

def basket(request, add_id=None):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    if add_id:
        if not request.user.is_authenticated:
            messages.error = get_error_message("not_authenticated", request)
            return redirect(request.META.get("HTTP_REFERER", "home"))
        product = Product.objects.filter(id=add_id, deleted=False).first()
        if not product:
            messages.error = get_error_message("product_not_found", request)
            return redirect(request.META.get("HTTP_REFERER", "home"))
        cart, created = Cart.objects.get_or_create(user=request.user, product=product, status=True)
        if not created:
            messages.error = get_error_message("already_in_cart", request)
        else:
            messages.error = get_error_message("cart_added", request)
        return redirect("basket")
    carts = Cart.objects.filter(user=request.user, status=True) if request.user.is_authenticated else []
    return render(request, 'pages/basket.html', {"carts": carts, "lang": lang, "basket_count": carts.count()})

def change_cart(request, cart_id, inc):
    cart = Cart.objects.filter(id=cart_id, user=request.user).first()
    if cart:
        if inc:
            cart.quantity += 1
        else:
            cart.quantity = max(1, cart.quantity - 1)
        cart.save()
        return JsonResponse({"success": "Muaffaqiyatli!", "total_balance": request.user.calculate_cart()})
    return JsonResponse({"error": "Cart Topilmadi"})

@require_POST
def cart_add(request, add_id):
    if not request.user.is_authenticated:
        messages.error = get_error_message("not_authenticated", request) or "Пожалуйста, войдите для добавления в корзину!"
        return redirect(request.META.get("HTTP_REFERER", "products"))

    product = Product.objects.filter(id=add_id).first()
    if not product:
        messages.error = get_error_message("product_not_found", request) or "Товар не найден!"
        return redirect(request.META.get("HTTP_REFERER", "products"))

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product, status=True)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.error = get_error_message("already_in_cart", request) or "Товар уже в корзине, количество обновлено!"
        return redirect(request.META.get("HTTP_REFERER", "products"))

    messages.error = get_error_message("cart_added", request) or "Товар успешно добавлен в корзину!"
    return redirect(request.META.get("HTTP_REFERER", "products"))

@login_required
def cart_remove(request, remove_id):
    product = Product.objects.filter(id=remove_id, deleted=False).first()
    if product:
        Cart.objects.filter(user=request.user, product=product, status=True).delete()
    return redirect(request.META.get("HTTP_REFERER", "products"))

@require_POST
@csrf_exempt
def login_view(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next") or "/"
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True, "next": next_url})
        return JsonResponse({"success": False, "error": get_error_message("login_failed", request)})
    return JsonResponse({"success": False, "error": "Invalid request method"})

@require_POST
@csrf_exempt
def register_view(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        if not all([name, phone, password]):
            return JsonResponse({"success": False, "error": "Заполните все поля"})
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({"success": False, "error": get_error_message("phone_already_exists", request)})
        user = User.objects.create_user(phone=phone, username=name, password=password)
        login(request, user)
        return JsonResponse({"success": True, "next": "/"})
    return JsonResponse({"success": False, "error": "Invalid request method"})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, get_error_message("logout_success", request))
    return redirect("home")

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
            return JsonResponse({"success": False, "message": "Заполните все обязательные поля!"})

        product = Product.objects.get(id=product_id, deleted=False)
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            full_name=full_name,
            phone=phone,
            email=email,
            additional_info=additional_info
        )
        return JsonResponse({"success": True, "message": get_error_message("order_success", request) or "Order placed successfully!"})
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": get_error_message("product_not_found", request)})
    except ValueError:
        return JsonResponse({"success": False, "message": "Неверное количество!"})
    except Exception as e:
        return JsonResponse({"success": False, "message": get_error_message("invalid_request", request) or f"Error: {str(e)}"})

@require_GET
def get_brands(request):
    return JsonResponse(list(Brand.objects.values('id', 'name')), safe=False)

@require_GET
def reset_filters(request):
    lang = request.session.get('lang', 'uz')
    return redirect(f'/products/?lang={lang}')

@require_GET
def get_models(request):
    return JsonResponse(list(CarModel.objects.filter(deleted=False).values('id', 'name')), safe=False)

@require_GET
def get_years(request):
    model_id = request.GET.get('model_id')
    years = CarYear.objects.filter(deleted=False).values('id', 'year').order_by('year')
    if model_id:
        years = years.filter(model_id=model_id)
    return JsonResponse(list(years), safe=False)

@require_GET
def get_series(request):
    year_id = request.GET.get('year_id')
    series = CarSeries.objects.filter(deleted=False).values('id', 'name')
    if year_id:
        series = series.filter(year_id=year_id)
    return JsonResponse(list(series), safe=False)





