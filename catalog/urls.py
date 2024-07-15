from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from catalog.apps import CatalogConfig
from catalog import views
from config.settings import DEBUG

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:pk>/", views.detail, name="detail"),
    path("add/", views.add_product, name="add"),
    path("contacts/", views.contacts, name="contacts"),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
