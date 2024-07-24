from django.core.mail import EmailMessage
from pytils.translit import slugify

from config.settings import EMAIL_ADMIN


def generate_slug(model, title):
    """
    Генерирует slug, добавляет цифру, если такой есть в базе
    """
    slug = slugify(title)
    while model.objects.filter(slug=slug).exists():
        if slug[-1].isdigit():
            number = ""
            for char in slug[::-1]:
                if char.isdigit():
                    number += char
                else:
                    break
            suffix = str(int(number[::-1]) + 1)
            slug = slug[: -len(number)] + suffix
        else:
            slug += "1"
    return slug


def send_congratulation(article):
    """
    Отправляет письмо с поздравлениями
    """

    text = f'Статья "{article.title.capitalize()}" уже имеет 100 просмотров!'

    email = EmailMessage(
        subject="Поздравление",
        body=text,
        to=(EMAIL_ADMIN,),
    )
    email.send(fail_silently=False)
