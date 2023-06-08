from django import forms
from .models import Customer, Supplier, Operation, Item


class CustomerForm(forms.ModelForm):
    choices = (
        ('1', 'Физ. лицо/ИП'),
        ('2', 'ТОО'),
        ('3', 'АО, страховая компания'),
        ('4', 'НАО "Правительство для граждан"'),
        ('5', 'Банк'),
        ('6', 'Иностранная фирма'),
        ('7', 'Управление гос. доходов'),
    )
    type = forms.ChoiceField(choices=choices)

    class Meta:
        model = Customer
        fields = '__all__'
        labels = {
            'name': 'Наименование',
            'type': 'Тип',
            'address': 'Адрес',
            'phone': 'Телефон',
            'email': 'Почта',
            'bin': 'БИН/ИИН'
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        labels = {
            'name': 'Наименование',
            'is_payment': 'Подлежит оплате',
            'is_bank': 'ТБС',
            'amount': 'Количество',
            'price': 'Цена',
            'item': 'Товар',
            'supplier': 'Поставщик',
        }
        exclude = []


class RevenueForm(OperationForm):
    is_sale = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
        initial=False
    )

    def __init__(self, *args, **kwargs):
        super(RevenueForm, self).__init__(*args, **kwargs)
        self.fields['supplier'] = forms.ModelChoiceField(queryset=Supplier.objects.all())
        self.fields['supplier'].empty_label = 'Поставщик не выбран'
        self.fields['item'].empty_label = 'Товар не выбран'
        self.fields['supplier'].label = 'Поставщик'
    class Meta(OperationForm.Meta):
        model = Operation
        exclude = OperationForm.Meta.exclude + ['customer', ]


class SaleForm(OperationForm):
    is_sale = forms.BooleanField(
        widget=forms.HiddenInput(),
        initial=True
    )
    is_payment = forms.BooleanField(
        widget=forms.HiddenInput(),
        initial=False
    )

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['customer'] = forms.ModelChoiceField(queryset=Customer.objects.all())
        self.fields['customer'].empty_label = 'Покупатель не выбран'
        self.fields['customer'].label = 'Покупатель'
        self.fields['item'].empty_label = 'Товар не выбран'

    class Meta(OperationForm.Meta):
        model = Operation
        exclude = OperationForm.Meta.exclude + ['supplier']

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = []