from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Cake
from decimal import Decimal
from .forms import CartAddCake

# Create your views here.
# Rewrite views


def get_or_create_cart(request):
    cart = request.session.get(settings.CART_DATA)
    if not cart:
        cart = request.session[settings.CART_DATA] = {}
    return cart


def add_cake(request, cake_id):
    """ Adding cake to the cart"""
    cake = Cake.objects.get(id=cake_id)
    cake_id = str(cake_id)
    cart = get_or_create_cart(request)
    form = CartAddCake(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        if cake_id not in cart:
            cart[cake_id] = {
                'quantity': 0,
                'price': str(cake.price)
            }

        if request.POST.get('quantity_update'):
            cart[cake_id]['quantity'] = cd['quantity']
        else:
            cart[cake_id]['quantity'] += cd['quantity']

        request.session.modified = True

    return redirect('cart:detail_page_cart')


def detail_page_cart(request):
    cart = get_or_create_cart(request)
    cake_ids = cart.keys()
    cakes = Cake.objects.filter(id__in=cake_ids)
    temp_cart = cart.copy()

    for cake in cakes:
        cart_item = temp_cart[str(cake.id)]
        cart_item['cake'] = cake
        cart_item['total_price'] = (Decimal(cart_item['price']) * cart_item['quantity'])
        cart_item['update_quantity_form'] = CartAddCake(initial={
            'quantity': cart_item['quantity']
        })

    cart_total_price = sum(Decimal(item['price']) * item['quantity']
                           for item in temp_cart.values())

    return render(
        request,
        'cart/cart.html',
        {
            'cart': temp_cart.values(),
            'cart_total_price': cart_total_price
        })


def delete_cake(request, cake_id):
    cart = get_or_create_cart(request)
    cake_id = str(cake_id)
    if cake_id in cart:
        del cart[cake_id]

        request.session.modified = True

        return redirect('cart:detail_page_cart')


def cart_clear(request):
    del request.session[settings.CART_DATA]
