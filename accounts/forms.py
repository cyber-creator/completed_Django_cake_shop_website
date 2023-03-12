from django import forms
from django.contrib.auth.models import User
from .models import Profile


class FormRegister(forms.ModelForm):
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class FormLogin(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class FormProfile(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'address', 'postal_code', 'city', 'state')


class FormUser(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class FormChangePassword(forms.Form):

    passwordOld = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'profile-pass-current', 'type': 'password',
                                                                    'name': 'old_pass', 'class': 'profile-info__input'}))

    passwordNew = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'profile-pass-new', 'type': 'password',
                                                                    'name': 'new_pass', 'class': 'profile-info__input'}))

    passwordConf = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'profile-pass-confirm', 'type': 'password',
                                                                     'name': 'confirm_pass', 'class': 'profile-info__input'}))
