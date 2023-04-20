from datetime import datetime
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


def get_operations_total(operation_type, is_last_month=False):
    if not is_last_month:
        return Operation.objects.filter(is_sale=operation_type).aggregate(Sum('amount'))['amount__sum']
    else:
        res = Operation.objects.filter(is_sale=operation_type, time__month=str(datetime.now().month)).aggregate(
            Sum('amount'))['amount__sum']
        if res is None:
            return 0
        else:
            return res


def get_operations_by_source(operation_type, is_bank, is_last_month=False):
    if not is_last_month:
        return Operation.objects.filter(is_sale=operation_type, is_bank=is_bank).aggregate(Sum('amount'))['amount__sum']
    else:
        res = Operation.objects.filter(is_sale=operation_type, is_bank=is_bank,
                                       time__month=str(datetime.now().month)).aggregate(
            Sum('amount'))['amount__sum']
        if res is None:
            return 0
        else:
            return res


def get_today_operations(operation_type, is_bank):
    today = datetime.now().day
    print(today)
    res = Operation.objects.filter(is_sale=operation_type, is_bank=is_bank,
                                   time__day=today).aggregate(
        Sum('amount'))['amount__sum']
    if res is None:
        return 0
    else:
        return res


def get_charts_data():
    request = Operation.objects.all()
    today = datetime.now().date()
    data = {
        'today': {
            'sales': {
                'total':  Operation.objects.filter(
                    is_sale=True,
                    time=today
                ).aggregate(Sum('amount'))['amount__sum'],
                'bank': '228',
                'cash': '322',
            },
            'revenue': {
                'total': '1337',
                'bank': '228',
                'cash': '322',
            }
        },
        'month': {
            'sales': {
                'total': request.filter(is_sale=True).aggregate(Sum('amount'))['amount__sum'],
                'bank': request.filter(is_sale=True, is_bank=True).aggregate(Sum('amount'))['amount__sum'],
                'cash': request.filter(is_sale=True, is_bank=False).aggregate(Sum('amount'))['amount__sum'],
            },
            'revenue': {
                'total': request.filter(is_sale=False).aggregate(Sum('amount'))['amount__sum'],
                'bank': request.filter(is_sale=False, is_bank=True).aggregate(Sum('amount'))['amount__sum'],
                'cash': request.filter(is_sale=False, is_bank=False).aggregate(Sum('amount'))['amount__sum'],
            }
        }
    }
    print(data['today'])
    return data
