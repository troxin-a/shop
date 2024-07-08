from pyclbr import Class
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        **NULLABLE,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание продукта",
        **NULLABLE,
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        help_text="Выберите изображение продукта",
        **NULLABLE,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите категорию продукта",
        **NULLABLE,
    )
    price = models.IntegerField(
        verbose_name="Цена",
        help_text="Введите цену продукта",
        default=0,
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)


class Contacts(models.Model):
    address = models.TextField(
        verbose_name="Адрес",
        help_text="Введите адрес",
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        help_text="Введите Телефон",
    )
    email = models.EmailField(
        verbose_name="email",
        help_text="Введите email",
    )

    def __str__(self) -> str:
        return self.address

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "Контакты"
