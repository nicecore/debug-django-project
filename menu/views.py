from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Menu
from .forms import MenuForm

def menu_list(request):
    # Fetch all menus in a queryset
    all_menus = Menu.objects.all().prefetch_related('items')

    # Declare empty list 'menus' and append to it all menus that haven't expired
    menus = []
    for menu in all_menus:
        menus.append(menu)

    return render(request, 'menu/all_menus.html', {'menus': menus})


def menu_detail(request, pk):
    # Retrieve a menu object by pk, send to template
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/item_detail.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/new_menu.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=form.instance.pk)
    return render(request, 'menu/edit_menu.html', {'form': form})




















