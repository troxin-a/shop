from django.core.cache import cache
from catalog.models import Category, Product, Version
from config import settings


def get_categories_from_cache():
    """Получает queryset категорий из кеша, либо делает запрос в БД"""

    if settings.CACHE_ENABLED:
        key = "categories_list"
        categories = cache.get(key)
        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories)
    else:
        categories = Category.objects.all()

    return categories


def get_product_counts_by_category_from_cache(category):
    """Получает количество товаров в категории из кеша, либо делает запрос в БД"""

    if settings.CACHE_ENABLED:
        key = f"product_count_{category.pk}"
        product_count = cache.get(key)
        if product_count is None:
            product_count = category.products.filter(is_published=True).count()
            cache.set(key, product_count)
    else:
        product_count = category.products.filter(is_published=True).count()

    return product_count


def get_products_by_category(category_id):
    """Получает опубликованные продукты из БД по категории"""
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    else:
        products = Product.objects.all()

    return products.filter(is_published=True)


def get_products_from_cache(category_id=None):
    """
    Получает queryset опубликованных продуктов из кеша, либо делает запрос в БД
    Принимает category_id и фильтрует. Если None - не фильтрует
    """

    if settings.CACHE_ENABLED:
        key = f"product_list_{category_id}"
        products = cache.get(key)
        if products is None:
            products = get_products_by_category(category_id)
            cache.set(key, products)
    else:
        products = get_products_by_category(category_id)

    return products


def get_version_from_cache(product_id):
    """
    Получает версию продукта из кеша, либо делает запрос в БД
    """

    if settings.CACHE_ENABLED:
        key = f"current_version_product_{product_id}"
        version = cache.get(key)
        if version is None:
            version = Version.objects.filter(product__id=product_id, is_current=True).last()
            if version is None:
                version = 0
            cache.set(key, version)
    else:
        version = Version.objects.filter(product__id=product_id, is_current=True).last()

    return version
