import json
import os
from django.core.management import BaseCommand

from catalog.models import Category, Contacts, Product
from config.settings import BASE_DIR


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open(
            os.path.join(BASE_DIR, "fixtures", "catalog", "cats.json"), encoding="UTF-8"
        ) as file:
            return json.load(file)

    @staticmethod
    def json_read_products():
        with open(
            os.path.join(BASE_DIR, "fixtures", "catalog", "products.json"),
            encoding="UTF-8",
        ) as file:
            return json.load(file)
        
    @staticmethod
    def json_read_contacts():
        with open(
            os.path.join(BASE_DIR, "fixtures", "catalog", "contacts.json"),
            encoding="UTF-8",
        ) as file:
            return json.load(file)

    def handle(self, *args, **options):

        # Удаляем все продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()
        Contacts.objects.all().delete()

        # Пустые списки для хранения объектов
        product_for_create = []
        category_for_create = []
        contacts_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            name = category["fields"].get("name")
            description = category["fields"].get("description")
            category_for_create.append(
                Category(name=name, description=description, pk=category["pk"])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            name = product["fields"].get("name")
            description = product["fields"].get("description")
            image = product["fields"].get("image")
            # получаем категорию из базы данных для корректной связки объектов
            category = Category.objects.get(id=product["fields"].get("category"))
            price = product["fields"].get("price")
            created_at = product["fields"].get("created_at")
            updated_at = product["fields"].get("updated_at")

            product_for_create.append(
                Product(
                    name=name,
                    description=description,
                    image=image,
                    category=category,
                    price=price,
                    created_at=created_at,
                    updated_at=updated_at,
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)


        # Обходим все значения контактов из фиктсуры для получения информации об одном объекте
        for contact in Command.json_read_contacts():
            address = contact["fields"].get("address")
            phone = contact["fields"].get("phone")
            email = contact["fields"].get("email")
            contacts_for_create.append(
                Contacts(address=address, phone=phone, email=email)
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Contacts.objects.bulk_create(contacts_for_create)
