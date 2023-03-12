from django import forms
from django.forms import NumberInput


class CartAddCake(forms.Form):
    quantity = forms.IntegerField(min_value=1)


