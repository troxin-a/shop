# Generated by Django 5.0.6 on 2024-07-24 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Arcticle',
            new_name='Article',
        ),
    ]
