from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.detail_page_cart, name='detail_page_cart'),
    path('add-cake/<int:cake_id>/', views.add_cake, name='add_cake_to_cart'),
    path('delete-cake/<int:cake_id>/', views.delete_cake, name='delete_cake_from_cart'),
]
