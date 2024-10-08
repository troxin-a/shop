# Generated by Django 4.2.9 on 2024-08-14 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.CharField(max_length=150, unique=True, verbose_name='slug')),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='blog', verbose_name='Превью')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('published_at', models.DateField(blank=True, null=True, verbose_name='Дата публикации')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликован')),
                ('views_count', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'статью',
                'verbose_name_plural': 'Статьи',
                'ordering': ('id',),
            },
        ),
    ]
