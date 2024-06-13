from django.contrib import admin
from .models import Supplier, Item, Inventory, Warehouse

# Register your models here.

admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(Warehouse)
