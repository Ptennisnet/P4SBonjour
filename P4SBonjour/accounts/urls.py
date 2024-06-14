from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('login_incorrect/', views.login_incorrect_view, name='login_incorrect'),
    path('login_lockout/', views.login_lockout_view, name='login_lockout'),
    path('logout/', views.logout_view, name='logout'),
    path('send_mfa_code/', views.send_mfa_code, name='send_mfa_code'),
    path('verify_mfa/', views.verify_mfa, name='verify_mfa'),
]
