from cart.views import get_or_create_cart
from decimal import Decimal


def cart_label(request):
    cart = get_or_create_cart(request)
    cart_total = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())

    return {
        'cart_total': cart_total,
    }