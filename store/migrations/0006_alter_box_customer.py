# Generated by Django 4.1.2 on 2022-10-06 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_storage_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='customer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer', verbose_name='Клиент'),
        ),
    ]