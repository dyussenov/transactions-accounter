# Generated by Django 4.2 on 2023-06-08 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounter', '0011_operation_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(default='no address', max_length=55),
        ),
    ]
