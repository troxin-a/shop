from django.db import models

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории", **NULLABLE,
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
        verbose_name="Описание", help_text="Введите описание продукта", **NULLABLE,
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
        verbose_name="Цена", help_text="Введите цену продукта", default=0,
    )
    created_at = models.DateField(
        auto_now_add=True, editable=False, verbose_name="Дата создания",
    )
    updated_at = models.DateField(
        auto_now=True, editable=False, verbose_name="Дата изменения",
    )
    manufactured_at = models.DateField(
        verbose_name="Дата производства",
        **NULLABLE,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)
