from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from cart.forms import CartAddCake
from .models import Category, Cake, Review
from .forms import FormReview, ContactForm

# Create your views here.


def use_pagination(request, cakes):
    paginator = Paginator(cakes, 3)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj


def all_cakes(request, selected_category=None):
    categories = Category.objects.all()
    cakes = Cake.objects.all()
    new_cakes = cakes.order_by('-id')[:3]
    filtered_cake_by_category = None

    if selected_category:
        filtered_cake_by_category = get_object_or_404(Category, slug=selected_category)
        cakes = Cake.objects.filter(category=filtered_cake_by_category)

    cakes_paginator = use_pagination(request, cakes)

    context = {'categories': categories, 'filtered_cake_by_category': filtered_cake_by_category,
               'cakes': cakes_paginator, 'new_cakes': new_cakes}
    return render(request, 'catalog/index.html', context)


def filter_price(request):
    category = Category.objects.all()
    cakes = Cake.objects.all()
    new_cakes = cakes.order_by('-id')[:3]

    context = {'categories': category, 'cakes': cakes, 'new_cakes': new_cakes}

    if request.method == "GET":

        if request.GET.get('selected'):
            filtered_cake_by_category = category.get(id=request.GET.get('selected'))
            cakes = cakes.filter(category=filtered_cake_by_category)
            context['filtered_cake_by_category'] = filtered_cake_by_category

        if request.GET.get('get_start_price'):
            get_start_price = request.GET.get('get_start_price')
            get_end_price = request.GET.get('get_end_price')
            cakes = cakes.filter(price__range=(get_start_price, get_end_price))

            context['get_start_price'] = get_start_price
            context['get_end_price'] = get_end_price

        cakes_paginator = use_pagination(request, cakes)
        context['cakes'] = cakes_paginator

    return render(request, 'catalog/index.html', context)


def cake_single(request, cake_slug):
    cake = get_object_or_404(Cake, slug=cake_slug)
    new_cakes = Cake.objects.all().order_by('-id')[:3]

    if request.POST.get("review_update"):
        review_update = Review.objects.get(id=int(request.POST.get("review_update")))
        if request.user == review_update.user:
            form = FormReview(request.POST, instance=review_update)
            form.save()
        return redirect(cake.get_absolute_url())

    if request.method == "POST":
        form = FormReview(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            rf = form.cleaned_data
            author = request.user.username
            current_user = request.user

            Review.objects.create(
                user=current_user,
                cake=cake,
                author=author,
                review=rf['review'],
                rating=float(rf['rating'])
            )
            return redirect(cake.get_absolute_url())
        else:
            form_review = FormReview()
            cart_form = CartAddCake()

            return render(
                request,
                'pages/single.html',
                {
                    'cake': cake,
                    'form_review': form_review,
                    'cart_form': cart_form,
                }
            )

    return render(request, 'pages/single.html', {'cake': cake, 'new_cakes': new_cakes})


def about_page(request):
    return render(request, 'pages/about.html')


def contact_page(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            cf = contact_form.cleaned_data
            name = cf['name']
            email = cf['email']
            phone = cf['phone_number']
            message = cf['subject']
            send_to = 'kirkevich.anton@gmail.com'

            template = render_to_string('pages/contact_email.html', {'email': email, 'name': name, 'phone': phone,
                                                                     'message': message})

            email = EmailMessage(
                'Cake Customer Email',
                template,
                settings.EMAIL_HOST_USER,
                [send_to],
            )

            email.fail_silently = False
            email.send()

            contact_form.save()

    return render(request, 'pages/contact.html')


@login_required
def delete_review(request):
    if request.method == 'POST':
        review_to_delete = get_object_or_404(Review, id=request.POST["review"])

        if review_to_delete.user == request.user:
            review_to_delete.delete()

    return redirect(request.META['HTTP_REFERER'], permanent=True)
