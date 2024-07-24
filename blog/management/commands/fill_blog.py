import json
import os
from django.core.management import BaseCommand

from blog.models import Article
from config.settings import BASE_DIR


class Command(BaseCommand):

    @staticmethod
    def json_read_articles():
        with open(
            os.path.join(BASE_DIR, "fixtures", "blog", "articles.json"), encoding="UTF-8"
        ) as file:
            return json.load(file)


    def handle(self, *args, **options):

        # Удаляем все статьи
        Article.objects.all().delete()


        # Пустой список для хранения объектов
        artiecle_for_create = []


        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for article in Command.json_read_articles():
            title = article["fields"].get("title")
            slug = article["fields"].get("slug")
            content = article["fields"].get("content")
            preview = article["fields"].get("preview")
            created_at = article["fields"].get("created_at")
            published_at = article["fields"].get("published_at")
            is_published = article["fields"].get("is_published")
            views_count = article["fields"].get("views_count")

            artiecle_for_create.append(
                Article(
                    title=title,
                    slug=slug,
                    content=content,
                    preview=preview,
                    created_at=created_at,
                    published_at=published_at,
                    is_published=is_published,
                    views_count=views_count,
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Article.objects.bulk_create(artiecle_for_create)
