# Generated by Django 5.0.6 on 2024-08-06 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_category_options_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название версии'),
        ),
        migrations.AlterField(
            model_name='version',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='catalog.product', verbose_name='Продукт'),
        ),
    ]
