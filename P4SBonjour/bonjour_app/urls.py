from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_item, name='add_item'),
    path('view/<int:item_id>/', views.view_item, name='view_item'),
]