from django import forms
from .models import Supplier, Item, Warehouse, Inventory


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'contact_info']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'description', 'supplier']


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['warehouse_name', 'location']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item', 'warehouse', 'quantity']
