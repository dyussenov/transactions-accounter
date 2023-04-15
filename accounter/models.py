from django.db import models


class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=60)
    address = models.CharField(unique=False, default='no address', max_length=120)
    phone = models.CharField(unique=False, max_length=15)
    email = models.EmailField(max_length=60)


class Customer(models.Model):
    name = models.CharField(unique=True, max_length=60)
    type = models.CharField(unique=False, max_length=20)
    address = models.CharField(unique=False, default='no address', max_length=20)
    phone = models.CharField(unique=False, max_length=15)
    email = models.EmailField(max_length=60)


class Operation(models.Model):
    name = models.CharField(unique=False, max_length=120)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(unique=False, max_length=20)
    source = models.CharField(unique=False, max_length=20)
    amount = models.IntegerField()
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
