from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm

def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})


def view_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'view_item.html', {'item': item})