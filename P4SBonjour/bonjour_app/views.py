from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Supplier, Item, Inventory, Warehouse
from .forms import SupplierForm, ItemForm, WarehouseForm, InventoryForm


def staff_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_staff,
        login_url='/login/',
    )(view_func)
    return decorated_view_func


@login_required
def home(request):
    return render(request, 'home.html')


@staff_required
def update_database(request):
    return render(request, 'update_database.html')


@staff_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})


@staff_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = ItemForm()
        return render(request, 'add_item.html', {'form': form})
    else:
        form = ItemForm()
        return render(request, 'add_item.html', {'form': form})


@staff_required
def add_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = WarehouseForm()
        return render(request, 'add_warehouse.html', {'form': form})
    else:
        form = WarehouseForm()
        return render(request, 'add_warehouse.html', {'form': form})


@staff_required
def update_stock(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            warehouse = form.cleaned_data['warehouse']
            quantity = form.cleaned_data['quantity']

            inventory, created = Inventory.objects.update_or_create(
                item=item,
                warehouse=warehouse,
                defaults={'quantity': quantity}
            )
            return redirect('home')
        else:
            return render(request, 'update_stock.html', {'form': form})
    else:
        form = InventoryForm()
        return render(request, 'update_stock.html', {'form': form})


@login_required
def item_list(request):
    items = Item.objects.all()
    item_data = []
    for item in items:
        total_quantity = Inventory.objects.filter(item=item).aggregate(Sum('quantity'))['quantity__sum']
        if total_quantity is None:
            total_quantity = '-'
        item_data.append({
            'item': item,
            'total_quantity': total_quantity
        })
    return render(request, 'item_list.html', {'item_data': item_data})


@login_required
def view_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'view_item.html', {'item': item})


@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    supplier_data = []
    for supplier in suppliers:
        items_supplied = Item.objects.filter(supplier=supplier)
        supplier_data.append({
            'supplier': supplier,
            'items_supplied': items_supplied
        })
    return render(request, 'supplier_list.html', {'supplier_data': supplier_data})


@login_required
def view_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    items_supplied = Item.objects.filter(supplier=supplier)
    return render(request, 'view_supplier.html', {
        'supplier': supplier,
        'items_supplied': items_supplied
    })


@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse_list.html', {'warehouses': warehouses})


@login_required
def warehouse_summary(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    inventory_items = Inventory.objects.filter(warehouse=warehouse)
    return render(request, 'warehouse_summary.html', {
        'warehouse': warehouse,
        'inventory_items': inventory_items
    })


@login_required
def inventory_summary(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    inventories = Inventory.objects.filter(item=item)
    total_quantity = inventories.aggregate(Sum('quantity'))['quantity__sum'] or 0
    return render(request, 'inventory_summary.html', {
        'item': item,
        'inventories': inventories,
        'total_quantity': total_quantity
    })
