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
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
    )
    description = models.TextField(
        verbose_name="Описание",
        **NULLABLE,
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        **NULLABLE,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name="products",
        verbose_name="Категория",
        **NULLABLE,
    )
    price = models.IntegerField(
        verbose_name="Цена",
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


class Version(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name="Продукт",
        **NULLABLE,
    )
    number = models.PositiveIntegerField(
        verbose_name="Номер версии",
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Название версии",
    )
    is_current = models.BooleanField(verbose_name="Текущая", default=False)

    def __str__(self) -> str:
        return f"{self.number} - {self.name}"

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "Версии"
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
