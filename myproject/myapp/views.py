from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required, user_passes_test


def index(request):
    items = Item.objects.all()
    return render(request, 'myapp/index.html', {'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect('index')
    else:
        form = ItemForm()
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Добавить объект'})

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect('index')
    return render(request, 'myapp/confirm_delete.html', {'item': item})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
                form.save()
                return redirect('index')
    else:
        form = ItemForm(instance=item)
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Редактировать объект'})