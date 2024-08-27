from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from catalog.apps import CatalogConfig
from catalog import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="index"),
    path("products/", views.ProductListOwnerView.as_view(), name="product_list_owner"),
    path("product/<int:pk>/", cache_page(60)(views.ProductDetailView.as_view()), name="detail"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", views.ProductByCategoryListView.as_view(), name="products_by_category"),
    path("version-update/<int:pk>/", never_cache(views.VersionUpdateView.as_view()), name="version-update"),
    path("version-delete/<int:pk>/", views.VersionDeleteView.as_view(), name="version-delete"),
    path("product/<int:pk>/version-create/", never_cache(views.VersionCreateView.as_view()), name="version-create"),
    path("create/", never_cache(views.ProductCreateView.as_view()), name="create"),
    path("update/<int:pk>/", never_cache(views.ProductUpdateView.as_view()), name="update"),
    path("contacts/", views.ContactListView.as_view(), name="contacts"),
    path("delete/<int:pk>/", views.ProductDeleteView.as_view(), name="delete"),
]
