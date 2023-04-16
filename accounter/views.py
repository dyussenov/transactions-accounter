from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .services import add_operation, get_operations_total


def home(request):
    context = {
        'supplier_form': SupplierForm,
        'operation_from': OperationForm,
        'operations': Operation.objects.all(),
        'total_sales': get_operations_total(True),
        'total_revenue': get_operations_total(False)
    }
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
