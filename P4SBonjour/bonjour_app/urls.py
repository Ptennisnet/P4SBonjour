from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_supplier, name='add_supplier'),
    path('view_supplier/', views.view_supplier, name='view_supplier'),
]
