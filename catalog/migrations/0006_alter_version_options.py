# Generated by Django 4.2.9 on 2024-08-20 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='version',
            options={'ordering': ('-id',), 'verbose_name': 'версия', 'verbose_name_plural': 'Версии'},
        ),
    ]
