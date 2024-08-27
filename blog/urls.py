from django.urls import path
from django.views.decorators.cache import never_cache
from blog.apps import BlogConfig

from blog import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("my-blog", never_cache(views.ArticleListOwnerView.as_view()), name="my_blog"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="detail"),
    path("create/", never_cache(views.ArticleCreateView.as_view()), name="create"),
    path("update/<int:pk>/", never_cache(views.ArticleUpdateView.as_view()), name="update"),
    path("delete/<int:pk>/", views.ArticleDeleteView.as_view(), name="delete"),
]
