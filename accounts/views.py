from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from accounts.forms import FormRegister, FormProfile, FormUser, FormChangePassword
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from orders.models import Order
from .models import Profile
# Create your views here.


def account_register(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            last_name = cd['last_name']
            email = cd['email']
            password = cd['password']
            password2 = cd['password2']

            if User.objects.filter(username=cd['first_name']).exists():
                messages.error(request, 'This username name already in use')
                return redirect('catalog:cakes_catalog')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email already in use please log in or change your password')
                return redirect('catalog:cakes_catalog')

            if password == password2:
                new_account = User.objects.create_user(first_name=first_name, last_name=last_name, username=first_name,
                                                       email=email, password=password)
                Profile.objects.create(user=new_account, first_name=first_name, last_name=last_name, email=email,)
                login(request, new_account)
                return redirect('account_profile')
            else:
                messages.error(request, 'Password does\'t match')
                return redirect('catalog:cakes_catalog')

    return redirect('catalog:cakes_catalog')


def account_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email).username
        login_account = authenticate(request, username=user, password=password)

        if login_account:
            login(request, login_account)
            return redirect('catalog:cakes_catalog')

        return redirect('catalog:cakes_catalog')


@login_required
def account_profile(request):
    context = {}
    if request.method == 'POST' and "user_info" in request.POST:
        try:
            profile = Profile.objects.get(user=request.user)
            user = User.objects.get(email=request.POST['email'])
        except ObjectDoesNotExist:
            profile = None
            user = None

        if user.id == request.user.id:
            form_profile = FormProfile(instance=request.user.profile, data=request.POST)
            form_user = FormUser(instance=request.user, data=request.POST)

            if form_profile.is_valid():
                form_profile.save()
                context["profile_data"] = form_profile

            if form_user.is_valid():
                form_user.save()
                context["user_data"] = form_user

            return render(request, 'account/profile.html', context)

    elif request.method == 'POST' and 'change' in request.POST:
        form = FormChangePassword(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            try:
                user = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                return redirect('account_login')

            if user:
                old_password = cd['passwordOld']
                new_password = cd['passwordNew']
                confirm_password = cd['passwordConf']

                if user.check_password(old_password) and new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Password was update')
                else:
                    messages.error(request, 'Sorry something don\'t match')
                return redirect('account_profile')

    else:
        form_profile = FormProfile(instance=request.user.profile)
        password_update = FormChangePassword()
        form_user = FormUser(instance=request.user)
        context["password_update"] = password_update
        context["profile_data"] = form_profile
        context["user_data"] = form_user

    return render(request, 'account/profile.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('catalog:cakes_catalog')


@login_required
def account_order(request, pk):
    context = {}
    order = Order.objects.get(id=pk)
    if order.user is None:
        return redirect('account_profile')
    elif request.user.email == order.user.email:
        context['order'] = order
        return render(request, 'account/order_detail.html', context)

    return redirect('account_profile')
