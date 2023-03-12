from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('new_order/', views.creating_order, name='new_order'),
]
