from django.urls import path
from catalog.apps import CatalogConfig
from catalog import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="index"),
    path("products/", views.ProductListOwnerView.as_view(), name="product_list_owner"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("version-update/<int:pk>", views.VersionUpdateView.as_view(), name="version-update"),
    path("version-delete/<int:pk>", views.VersionDeleteView.as_view(), name="version-delete"),
    path("product/<int:pk>/version-create/", views.VersionCreateView.as_view(), name="version-create"),
    path("create/", views.ProductCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.ProductUpdateView.as_view(), name="update"),
    path("contacts/", views.ContactListView.as_view(), name="contacts"),
    path("delete/<int:pk>/", views.ProductDeleteView.as_view(), name="delete"),
]
