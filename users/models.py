from django.contrib.auth.models import AbstractUser

from django.db import models
from django_countries.fields import CountryField

from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Почта", unique=True)
    avatar = models.ImageField(verbose_name="Аватар", upload_to="users/", **NULLABLE)
    phone = PhoneNumberField(verbose_name="Телефон", **NULLABLE)
    country = CountryField(verbose_name="Страна", blank_label="(Выберите страну)", **NULLABLE)
    token = models.CharField(max_length=16, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [""]
    
