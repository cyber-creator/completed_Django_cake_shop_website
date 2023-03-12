from django.urls import path
from . import views
from django.contrib.auth import views as authentication_views


urlpatterns = [
    path('register/', views.account_register, name='account_register'),
    path('login/', views.account_login, name='account_login'),
    path('profile/', views.account_profile, name='account_profile'),
    path('profile/order/<int:pk>', views.account_order, name='profile_order_detail'),
    path('logout/', views.logout_user, name='account_logout'),
    path('password_reset/', authentication_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', authentication_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', authentication_views.PasswordResetConfirmView.as_view(),
    name='password_reset_confirm'),
    path('password_reset/complete/', authentication_views.PasswordResetCompleteView.as_view(),
    name='password_reset_complete'),
]
