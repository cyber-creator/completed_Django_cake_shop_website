from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.all_cakes, name='cakes_catalog'),
    path('<slug:selected_category>', views.all_cakes, name="cakes_category"),
    path('filter/', views.filter_price, name='filter_by_price'),
    path('detail/<slug:cake_slug>', views.cake_single, name="single_cake"),
    path('delete_review/', views.delete_review, name="delete_review"),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
]
