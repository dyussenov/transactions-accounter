# Generated by Django 4.2 on 2023-04-15 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounter.customer'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounter.supplier'),
        ),
    ]
