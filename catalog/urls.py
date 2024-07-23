from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from catalog.apps import CatalogConfig
from catalog import views
from config.settings import DEBUG

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="index"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("create/", views.ProductCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.ProductUpdateView.as_view(), name="update"),
    path("contacts/", views.ContactListView.as_view(), name="contacts"),
    path("delete/<int:pk>/", views.ProductDeleteView.as_view(), name="delete"),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
