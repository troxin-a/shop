# Generated by Django 4.2.9 on 2024-08-14 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=50, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, help_text='Введите описание категории', null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(help_text='Введите адрес', verbose_name='Адрес')),
                ('phone', models.CharField(help_text='Введите Телефон', max_length=15, verbose_name='Телефон')),
                ('email', models.EmailField(help_text='Введите email', max_length=254, verbose_name='email')),
            ],
            options={
                'verbose_name': 'контакт',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Изображение')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер версии')),
                ('name', models.CharField(max_length=50, verbose_name='Название версии')),
                ('is_current', models.BooleanField(default=False, verbose_name='Текущая')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='catalog.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'Версии',
                'ordering': ('id',),
            },
        ),
    ]
