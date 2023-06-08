import json
import os
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from .forms import *
from .models import *
from .services import *

from django.http import FileResponse
from django.http import HttpResponse
from openpyxl import load_workbook
from io import BytesIO

def some_view(request, type):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="some_file_name.xlsx"'
    response.write(generate_report().getvalue())
    return response


def home(request):
    context = {
        'supplier_form': SupplierForm,
        'operation_from': OperationForm,
        'operations': Operation.objects.all(),
        'total_sales': get_operations_total(True),
        'total_revenue': get_operations_total(False),
        'sales_last_month': get_operations_total(True, True),
        'revenue_last_month': get_operations_total(False, True),
        'profit': get_operations_total(True, True) - get_operations_total(False, True),
        'total_sales_bank': get_operations_by_source(True, True),
        'total_sales_cash': get_operations_by_source(True, False),
        'total_revenue_bank': get_operations_by_source(False, True),
        'total_revenue_cash': get_today_operations(False, True),
    }
    context.update(get_charts_data())
    # за текущий день, банк/касса/приход/расход + нарастающий
    return render(request, 'accounter/home.html', context)


def customers(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {
        'customer_form': CustomerForm,
        'customers': Customer.objects.all()
    }
    return render(request, 'accounter/customers.html', context)


def suppliers(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers')

    context = {
        'supplier_form': SupplierForm,
        'suppliers': Supplier.objects.all()
    }
    return render(request, 'accounter/suppliers.html', context)


def transactions(request):
    context = {
        'revenue_from': RevenueForm,
        'sale_from': SaleForm,
        'operations': Operation.objects.all()
    }
    return render(request, 'accounter/operations.html', context)


def add_transaction(request, transaction_type):
    if request.method == 'POST':
        add_operation(request, transaction_type)
    return redirect('transactions')


def items(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')

    context = {
        'item_form': ItemForm,
        'items': Item.objects.all()
    }
    return render(request, 'accounter/items.html', context)


def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contracts')
    else:
        form = ContractForm()
    return render(request, 'accounter/contracts.html', {'form': form})


def download_file(request, pk):
    operation = get_object_or_404(Operation, pk=pk)
    file = operation.contract.contract_file.path
    response = FileResponse(open(file, 'rb'))
    return response


def generate_invoice(request, pk):
    operation = get_object_or_404(Operation, pk=pk)

    workbook = load_workbook(os.path.join(os.path.dirname(__file__), 'invoice.xlsx'))
    sheet = workbook.active

    cell = sheet['F22']
    cell.value = f'БИН/ИИН {operation.customer.bin},{operation.customer.name}, {operation.customer.address}, {operation.customer.phone}'

    stream = BytesIO()
    cell = sheet['I27']
    cell.value = f'{operation.item.name}'
    cell = sheet['T27']
    cell.value = f'{operation.amount}'
    sheet['AA27'] = f'{operation.price}'
    sheet['F24'] = f'{operation.contract}'
    sheet['B16'] = f'Счет на оплату № {operation.id}  от {operation.time.strftime("%Y-%m-%d %H:%M:%S")}'
    workbook.save(stream)
    stream.seek(0)
    response = HttpResponse(stream.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="имя_файла.xlsx"'
    return response
