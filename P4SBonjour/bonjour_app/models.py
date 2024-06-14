from django.db import models


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)
    contact_info = models.TextField()

    def __str__(self):
        return self.supplier_name


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255)
    location = models.TextField()

    def __str__(self):
        return self.warehouse_name


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name


class Inventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.item_name} in {self.warehouse.warehouse_name}: {self.quantity}"


