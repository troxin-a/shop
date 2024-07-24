from django.db import models

NULLABLE = {"null": True, "blank": True}


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    slug = models.CharField(max_length=150, verbose_name="slug", unique=True)
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(upload_to="blog", verbose_name="Превью", **NULLABLE)
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    published_at = models.DateField(
        verbose_name="Дата публикации",
        **NULLABLE,
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    views_count = models.IntegerField(
        verbose_name="Количество просмотров", default=0, **NULLABLE
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "статью"
        verbose_name_plural = "Статьи"
        ordering = ("id",)
