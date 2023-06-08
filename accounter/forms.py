from django import forms
from .models import Customer, Supplier, Operation, Item, Contract


class ContractForm(forms.ModelForm):
    contract_file = forms.FileField()
    contract_file.label = 'Файл'

    class Meta:
        model = Contract
        fields = '__all__'
        labels = {
            'name': 'Наименование',
        }


class CustomerForm(forms.ModelForm):
    choices = (
        ('Физ. лицо/ИП', 'Физ. лицо/ИП'),
        ('ТОО', 'ТОО'),
        ('АО, страховая компания', 'АО, страховая компания'),
        ('НАО "Правительство для граждан"', 'НАО "Правительство для граждан"'),
        ('Банк', 'Банк'),
        ('Иностранная фирма', 'Иностранная фирма'),
        ('Управление гос. доходов', 'Управление гос. доходов'),
    )
    type = forms.ChoiceField(choices=choices)
    type.label = 'Тип'

    class Meta:
        model = Customer
        fields = '__all__'
        labels = {
            'name': 'Наименование',
            'address': 'Адрес',
            'phone': 'Телефон',
            'email': 'Почта',
            'bin': 'БИН/ИИН'
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        labels = {
            'name': 'Наименование',
            'address': 'Адрес',
            'phone': 'Телефон',
            'email': 'Почта',
        }


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        labels = {
            'name': 'Наименование',
            'is_payment': 'Подлежит оплате',
            'is_bank': 'ТБС',
            'contract': 'Договор',
            'amount': 'Количество',
            'price': 'Цена',
            'item': 'Товар',
            'supplier': 'Поставщик',
        }
        exclude = ['total']


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
        initial=True
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
        labels = {
            'name': 'Наименование',
            'description': 'Описание',

        }
