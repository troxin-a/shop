from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = (
        (
            "title",
            "is_published",
        ),
        "slug",
        "content",
        "preview",
        "views_count",
        "created_at",
        "published_at",
    )
    readonly_fields = (
        "created_at",
        "views_count",
    )
    list_display = (
        "title",
        "created_at",
        "published_at",
        "is_published",
    )
    list_filter = ("is_published",)
    search_fields = (
        "title",
        "content",
    )
