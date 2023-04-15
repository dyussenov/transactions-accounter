from django import forms
from .models import Customer, Supplier, Operation


class CustomerForm(forms.ModelForm):
    choices = (
        ('1', 'Частное лицо'),
        ('2', 'Юридическое лицо')
    )
    type = forms.ChoiceField(choices=choices)

    class Meta:
        model = Customer
        fields = '__all__'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class OperationForm(forms.ModelForm):
    source_choices = (
        ('1', 'Банк'),
        ('2', 'Касса')
    )
    source = forms.ChoiceField(choices=source_choices)

    class Meta:
        model = Operation
        exclude = []


class RevenueForm(OperationForm):

    def __init__(self, *args, **kwargs):
        super(RevenueForm, self).__init__(*args, **kwargs)
        self.fields['supplier'] = forms.ModelChoiceField(queryset=Supplier.objects.all())
        self.fields['supplier'].empty_label = 'Заказчик не выбран'

    class Meta(OperationForm.Meta):
        model = Operation
        exclude = OperationForm.Meta.exclude + ['type', 'customer', ]


class SaleForm(OperationForm):
    type = forms.CharField(
        widget=forms.HiddenInput(),
        initial='Приход'
    )

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['customer'] = forms.ModelChoiceField(queryset=Customer.objects.all())
        self.fields['customer'].empty_label = 'Покупатель не выбран'

    class Meta(OperationForm.Meta):
        model = Operation
        exclude = OperationForm.Meta.exclude + ['supplier']
