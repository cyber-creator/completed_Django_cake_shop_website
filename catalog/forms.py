from django import forms
from .models import Review, Contact


class FormReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'review')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone_number', 'subject')
