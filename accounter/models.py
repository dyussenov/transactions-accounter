from django.db import models


class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=60)
    address = models.CharField(unique=False, default='no address', max_length=120)
    phone = models.CharField(unique=False, max_length=15)
    email = models.EmailField(max_length=60)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(unique=True, max_length=120)
    description = models.CharField(unique=True, max_length=360)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Customer(models.Model):
    name = models.CharField(unique=True, max_length=60)
    type = models.CharField(unique=False, max_length=20)
    address = models.CharField(unique=False, default='no address', max_length=20)
    phone = models.CharField(unique=False, max_length=15)
    email = models.EmailField(max_length=60)
    bin = models.CharField(max_length=25, default='0000')

    def __str__(self):
        return self.name


class Contract(models.Model):
    name = models.CharField(max_length=60, default="Без названия")
    contract_file = models.FileField(upload_to='contracts/')

    def __str__(self):
        return self.name


class Operation(models.Model):
    name = models.CharField(unique=False, max_length=120)
    time = models.DateTimeField(auto_now_add=True)
    is_sale = models.BooleanField(unique=False, default=False)
    is_payment = models.BooleanField(default=False)
    is_bank = models.BooleanField(unique=False, default=False)
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0, null=True)
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.total = self.price * self.amount
        super().save(*args, **kwargs)