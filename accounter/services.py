import io
import xlsxwriter
from datetime import datetime
from django.db.models import *

from .models import Operation
from .forms import *


def generate_report(report_type="today"):
    today = datetime.now().date()
    #operations = Operation.objects.filter(time__date=today)
    operations = Operation.objects.all()
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, f'Отчет по операциям за {today}')
    worksheet.write(1, 0, f'id')
    worksheet.write(1, 1, f'Наименование')
    worksheet.write(1, 2, f'Время')
    worksheet.write(1, 3, f'Контрагент')
    worksheet.write(1, 4, f'Тип')
    worksheet.write(1, 5, f'Сумма')
    worksheet.write(1, 6, f'Источник')
    line = 2
    for operation in operations:
        worksheet.write(line, 0, operation.id)
        worksheet.write(line, 1, operation.name)
        worksheet.write(line, 2, str(operation.time))
        worksheet.write(line, 3, 'unknown')
        worksheet.write(line, 4, operation.is_sale)
        worksheet.write(line, 5, operation.is_bank)
        worksheet.write(line, 6, operation.amount)
        line+=1
    
    workbook.close()
    return output


def add_operation(request, transaction_type):
    if transaction_type == 'sale':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form_errors = form.errors.as_data()
            print(form_errors)
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
    today = datetime.now().date()
    print(today)
    res = Operation.objects.filter(time__date=today).aggregate(
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
                'total': int(Operation.objects.filter(is_sale=True, time__date=today).aggregate(Sum('amount'))[
                                 'amount__sum'] or 0),
                'bank': int(
                    Operation.objects.filter(is_sale=True, is_bank=True, time__date=today).aggregate(Sum('amount'))[
                        'amount__sum'] or 0),
                'cash': int(
                    Operation.objects.filter(is_sale=True, is_bank=False, time__date=today).aggregate(Sum('amount'))[
                        'amount__sum'] or 0),
            },
            'revenue': {
                'total': int(Operation.objects.filter(is_sale=False, time__date=today).aggregate(Sum('amount'))[
                                 'amount__sum'] or 0),
                'bank': int(
                    Operation.objects.filter(is_sale=False, is_bank=True, time__date=today).aggregate(Sum('amount'))[
                        'amount__sum'] or 0),
                'cash': int(
                    Operation.objects.filter(is_sale=False, is_bank=False, time__date=today).aggregate(Sum('amount'))[
                        'amount__sum'] or 0),
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
