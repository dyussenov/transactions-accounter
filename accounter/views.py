import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .services import add_operation, get_operations_total, get_operations_by_source

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
def some_view(request, type):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    data = Operation.objects.all().values()
    for line in data:
        for k, v in line.items():
            print(v, end=',')
        print()

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


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
        'total_revenue_cash': get_operations_by_source(False, True),
    }
    #за текущий день, банк/касса/приход/расход + нарастающий
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
