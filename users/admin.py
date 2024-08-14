from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "country",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "country",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_editable = (
        "is_active",
    )
    exclude = (
        "password",
        "token",
    )
