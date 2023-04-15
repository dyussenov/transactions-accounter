from django.shortcuts import render

from .forms import *


def home(request):
    context = {
        'customer_form': CustomerForm,
        'supplier_form': SupplierForm,
        'operation_from': OperationForm
    }
    return render(request, 'accounter/home.html', context)
