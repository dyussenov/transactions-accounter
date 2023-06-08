# Generated by Django 4.2 on 2023-06-08 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounter', '0004_rename_source_operation_is_bank_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('description', models.CharField(max_length=360, unique=True)),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]