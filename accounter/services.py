from django.db.models import *

from .models import *
from .forms import *


def add_operation(request, transaction_type):
    if transaction_type == 'sale':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
    elif transaction_type == 'revenue':
        form = RevenueForm(request.POST)
        if form.is_valid():
            form.save()


def get_operations_total(operation_type):
    return Operation.objects.filter(is_sale=operation_type).aggregate(Sum('amount'))['amount__sum']