from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from core.auth import User
from core.error_messages import ERROR_MESSAGES
from core.forms import LoginForm, RegisterForm
from .models import Brand, Product, Cart, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate





def set_language(request, lang):
    request.session["lang"] = lang
    return redirect(request.META.get("HTTP_REFERER", "/"))

def get_error_message(code, request):
    lang = request.session.get("lang", "uz")  # по умолчанию узбекский
    return ERROR_MESSAGES.get(code, {}).get(lang, "Xatolik!")


def home(request):
    brands = Brand.objects.all()
    ctx = {"brands": brands}
    return render(request, 'pages/index.html', ctx)

def products(request):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    search = request.GET.get("search")
    products = Product.objects.all().prefetch_related('images')
    if search:
        products = products.filter(brand__slug=search)
    ctx = {
        "products": products,
        "lang": lang,
        "brands": Brand.objects.all(),
    }
    return render(request, 'pages/products.html', ctx)

def product_detail(request, pk):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    product_one = Product.objects.prefetch_related('images').filter(pk=pk).first()
    try:
        error = request.session.pop("error")
    except:
        error = None
    ctx = {
        "product_one": product_one,
        "lang": lang,
        "error": error
        
    }
    return render(request, 'pages/productDetails.html', ctx)



def basket(request, add_id=None):
    lang = request.GET.get('lang', request.session.get('lang', 'uz'))
    request.session['lang'] = lang
    if add_id:
        product = Product.objects.filter(id=add_id).first()

        if not product:
            messages.error(request, get_error_message("product_not_found", request))

            return redirect(request.META.get("HTTP_REFERER", "home"))



        cart = Cart.objects.filter(user=request.user, product=product).first()
        if cart:
            messages.error(request, get_error_message("already_in_cart", request))
            return redirect(request.META.get("HTTP_REFERER", "home"))

        Cart.objects.create(user=request.user, product=product)
        print('added')
        return redirect("cart")

    carts = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    print(carts.count())
    ctx = {
        "carts": carts,
        "lang": lang,
        "basket_count": carts.count()
    }
    return render(request, 'pages/basket.html', ctx)
def change_cart(request, cart_id, inc):
    cart = Cart.objects.filter(id=cart_id).first()
    if cart:
        if inc:
            cart.quantity += 1
        else:
            cart.quantity -= 1
        cart.save()
        return JsonResponse({
            "success": "Muaffaqiyatli!",
            "total_balance": request.user.calculate_cart()
        })
    else:
        return JsonResponse({
            "error": "Cart Topilmadi"
        })

@login_required
def cart_add(request, add_id):
    product = Product.objects.get(id=add_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect(request.META.get("HTTP_REFERER", "products"))

@login_required
def cart_remove(request, remove_id):
    product = Product.objects.get(id=remove_id)
    Cart.objects.filter(user=request.user, product=product).delete()
    return redirect(request.META.get("HTTP_REFERER", "products"))




def login_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Неверное имя или пароль"})


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if not (name and phone and password):
            return JsonResponse({"success": False, "error": "Заполните все поля"})

        if User.objects.filter(username=phone).exists():
            return JsonResponse({"success": False, "error": "Такой номер уже зарегистрирован"})

        user = User.objects.create_user(username=phone, first_name=name, password=password)
        login(request, user)
        return JsonResponse({"success": True})
    
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта")
    return redirect("home")