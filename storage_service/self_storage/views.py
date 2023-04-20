from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from random import randint, choice

from .models import Warehouse, Size, Box


def index(request):
    return render(request, template_name='index.html')


@login_required(login_url='/')
def my_rent(request):
    if request.GET:
        request.user.email = request.GET.get('EMAIL_EDIT')
        request.user.phone = request.GET.get('PHONE_EDIT')
        # request.user.set_password(request.GET.get('PASSWORD_EDIT'))
        # TODO if change password add redirect to login page, when create it
        request.user.save()
        return redirect('my_rent')
    orders = request.user.orders.all()  # TODO optimize query
    context = {"orders": orders}
    return render(request, template_name='my-rent.html', context=context)


# @login_required(login_url='/')
def boxes(request):
    index = 0
    warehouses_info = []

    all_warehouses = Warehouse.objects.all()
    
    warehouses_benefits = [
        'Рядом с метро',
        'Парковка',
        'Высокие потолки',
        'Большие боксы',
    ]

    for warehouse in all_warehouses:
        index += 1

        warehouse_info = {
            'index': index,
            'city': warehouse.name,
            'address': warehouse.address,
            'total_free_boxes': warehouse.boxes.filter(occupied=False).count(),
            'total_boxes': warehouse.boxes.count(),
            'price_from': 1000,
            'benefit': choice(warehouses_benefits),
            'max_height': randint(3, 6),
            'temperature': randint(10, 25)
        }

        warehouses_info.append(warehouse_info)

    boxes_volume_to_3 = []
    boxes_volume_to_10 = []
    boxes_volume_from_10 = []
    available_boxes = Box.objects.filter(occupied=False)

    for box in available_boxes:
        if box.size.name < 3:
            boxes_volume_to_3.append(box)
        elif box.size.name < 10:
            boxes_volume_to_10.append(box)
        elif box.size.name >= 10:
            boxes_volume_from_10.append(box)

    context = {
        'warehouses': warehouses_info,
        'available_boxes': available_boxes,
        "boxes_volume_to_3": boxes_volume_to_3,
        "boxes_volume_to_10": boxes_volume_to_10,
        "boxes_volume_from_10": boxes_volume_from_10,
    }

    return render(request, template_name='boxes.html', context=context)


def faq(request):
    return render(request, template_name='faq.html')
