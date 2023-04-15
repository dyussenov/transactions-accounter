from django.shortcuts import render, redirect

from .forms import *
from .models import *

def home(request):
    context = {
        'supplier_form': SupplierForm,
        'operation_from': OperationForm,
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
