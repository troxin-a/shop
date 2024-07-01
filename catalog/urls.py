from django.urls import path

from catalog.apps import CatalogConfig
from catalog import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts", views.contacts, name="contacts"),
]
