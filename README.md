# 🛒 Django Online-shop

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-4.2-brightgreen)

## 📦 О проекте

Этот проект представляет собой веб-приложение интернет-магазина, разработанное с использованием фреймворка Django. Он включает в себя основные функциональные возможности, такие как:

- Просмотр товаров
<!-- - Поиск и фильтрация -->
- Регистрация и авторизация пользователей
<!-- - Корзина покупок -->
<!-- - Оформление заказов -->
- Административная панель

## 🚀 Начало работы

Следуйте приведённым ниже инструкциям, чтобы запустить проект локально.

### Требования

- Python 3.10
- Django 4.2
- PostgreSQL (или другая поддерживаемая БД)

### Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/troxin-a/shop.git
cd shop
```

2. **Активируйте виртуальное окружение:**
```bash
poetry shell
```

3. **Установите зависимости:**
```bash
poetry install
```

4. **Создайте базу данных и примените миграции:**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

5. **Заполните настройки подключения к серверу в config/settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # пример с PostgreSQL
        'NAME': 'your_database', # Имя БД
        'HOST': 'localhost', # Адрес сервера БД
        'USER': 'your_user', # Имя владельца БД
        'PASSWORD': 'your_password', # Пароль владельца БД
        'PORT': 'your_port', # Если был изменен порт по умолчанию
    }
}
```

6. **Заполните настройки подключения к smtp-серверу в config/settings.py:**
```python
EMAIL_HOST = "smtp-server"
EMAIL_PORT = "port"
EMAIL_HOST_USER = "example@mail.com"
EMAIL_HOST_PASSWORD = "pass"
```

7. **Заполните базы несколькими товарами, если необходимо:**
```bash
python3 manage.py fill_blog
python3 manage.py fill_catalog
```

8. **Создайте суперпользователя для доступа к административной панели:**
```bash
python3 manage.py csu
```

9. **Запустите локальный сервер:**
```bash
python3 manage.py runserver
```

Теперь проект должен быть доступен по адресу http://127.0.0.1:8000/.

## 📚 Использование
Для использования функциональности административной панели перейдите по адресу http://127.0.0.1:8000/admin/ и войдите с данными своего суперпользователя. Либо авторизуйтесь на сайте, после чего в верхней панели отобразится ссылка "Админка".

## 🛠 Разработка
Если вы хотите внести свой вклад в проект, пожалуйста, следуйте этим шагам:

Создайте новую ветку:
```bash
git checkout -b feature/new-feature
```
Выполните необходимые изменения и зафиксируйте их:
``` bash
git commit -m "Add new feature"
```
Отправьте изменения в свою ветку:
```bash
git push origin feature/new-feature
```
Создайте pull request на GitHub.

## 📞 Контакты
Если у вас есть вопросы или предложения по улучшению проекта, вы можете связаться со мной по адресу pashinov24@gmail.com, либо в тг https://t.me/anton_pashinov.

Спасибо за внимание к нашему проекту! Удачи в разработке!