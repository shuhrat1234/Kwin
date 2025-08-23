from django.db.models import Sum

from core.models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        total_items = Cart.objects.filter(user=request.user).aggregate(
            total=Sum("quantity")
        )["total"] or 0
        return {"cart_count": total_items}
    return {"cart_count": 0}
