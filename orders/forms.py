from django import forms
from .models import Order, DeliveryOption, OrderStatus


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'postal_code',  'city', 'state', 'phone', 'email', 'note',
                  'delivery')
