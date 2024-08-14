from typing import Any
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args: Any, **options: Any) -> str | None:
        # User.objects.all().delete()
        user = User.objects.create(
            email="admin@leka.ru",
            first_name="Admin",
            last_name="Leka",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password("123qwe456rty")
        user.save()

        print("Admin is created: admin@leka.ru. Password: 123qwe456rty")
