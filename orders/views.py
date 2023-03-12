from decimal import Decimal
from django.shortcuts import render
from cart.views import get_or_create_cart, cart_clear
from orders.forms import CheckoutForm
from .models import *
from django.conf import settings
import stripe
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


stripe.api_key = settings.STRIP_SECRET_KEY


def creating_order(request):
    cart = get_or_create_cart(request)
    cake_ids = cart.keys()
    cakes = Cake.objects.filter(id__in=cake_ids)
    shipping_choices = DeliveryOption.objects.all()
    temp_cart = cart.copy()
    cart_total_price = sum(Decimal(item['price']) * item['quantity']
                           for item in temp_cart.values())

    for cake in cakes:
        cart_item = temp_cart[str(cake.id)]
        cart_item['cake'] = cake
        cart_item['total_price'] = (Decimal(cart_item['price']) * cart_item['quantity'])

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            new_order = form.save(commit=False)
            if request.user.is_authenticated:
                new_order.user = request.user

            delivery_obj = DeliveryOption.objects.get(id=int(request.POST.get("delivery")))
            shipping_price = delivery_obj.price
            final_price_with_shipping = shipping_price + cart_total_price
            new_order.shipping = shipping_price
            new_order.delivery = delivery_obj
            new_order.save()
            cakes = Cake.objects.filter(id__in=cart.keys())
            email = cd['email']

            for cake in cakes:
                cakes_in_cart = cart[str(cake.id)]

                OrderUnit.objects.create(order=new_order, cake=cake, price=cakes_in_cart['price'],
                                         quantity=cakes_in_cart['quantity'])

            customer = stripe.Customer.create(
                email=email,
                phone=cd['phone'],
                source=request.POST['stripeToken']
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=int(final_price_with_shipping * 100),
                currency='usd',
                description=new_order
            )

            template = render_to_string('pages/order_sent.html', {'email': email})

            email = EmailMessage(
                'Order processing',
                template,
                settings.EMAIL_HOST_USER,
                [email],
            )

            email.fail_silently = False
            email.send()

            cart_clear(request)
            return render(request, 'cart/completed.html', {'order': new_order, 'shipping': shipping_price,
                                                           'final_price_with_shipping': final_price_with_shipping})

    else:
        form = CheckoutForm()
        if request.user.is_authenticated:
            data = {
                'first_name': request.user.profile.first_name,
                'last_name': request.user.profile.last_name,
                'address': request.user.profile.address,
                'postal_code': request.user.profile.postal_code,
                'city': request.user.profile.city,
                'state': request.user.profile.state,
                'phone': request.user.profile.phone_number,
                'email': request.user.email,
            }
            form = CheckoutForm(initial=data)

    return render(request, 'cart/checkout.html', {'cart': cart, 'form': form,
                                                  'cart_items': temp_cart.values(),
                                                  'cart_total_price': cart_total_price,
                                                  'shipping_choices': shipping_choices})






