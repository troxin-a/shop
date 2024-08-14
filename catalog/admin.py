from django.contrib import admin

from catalog.models import Category, Product, Contacts, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = (
        "pk",
        "name",
        "price",
        "category",
        "owner",
    )
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("address", "phone", "email")


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("product", "number", "name", "is_current")
    list_filter = ("is_current",)
    search_fields = ("product",)
