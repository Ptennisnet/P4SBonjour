from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('add_item/', views.add_item, name='add_item'),
    path('view_item/<int:item_id>/', views.view_item, name='view_item'),
    path('add_warehouse/', views.add_warehouse, name='add_warehouse'),
    path('update_stock/', views.update_stock, name='update_stock'),
    path('item_list/', views.item_list, name='item_list'),
    path('inventory_summary/<int:item_id>/', views.inventory_summary, name='inventory_summary'),
    path('supplier_list/', views.supplier_list, name='supplier_list'),
    path('view_supplier/<int:supplier_id>/', views.view_supplier, name='view_supplier'),
    path('warehouse_list/', views.warehouse_list, name='warehouse_list'),
    path('warehouse_summary/<int:warehouse_id>/', views.warehouse_summary, name='warehouse_summary'),
]
