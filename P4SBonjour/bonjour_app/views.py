from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Supplier
from .forms import SupplierForm


@login_required
def home(request):
    suppliers = Supplier.objects.all()
    return render(request, 'home.html', {'suppliers': suppliers})


@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})


@login_required
def view_supplier(request):
    supplier_id = request.GET.get('supplier_id')
    supplier = get_object_or_404(Supplier, id=supplier_id)
    return render(request, 'view_supplier.html', {'supplier': supplier})
