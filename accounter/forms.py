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
    class Meta:
        model = Operation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OperationForm, self).__init__(*args, **kwargs)
        self.fields['customer'] = forms.ModelChoiceField(queryset=Customer.objects.all())
        self.fields['supplier'] = forms.ModelChoiceField(queryset=Supplier.objects.all())