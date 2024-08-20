from django.urls import path
from blog.apps import BlogConfig

from blog import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("my-blog", views.ArticleListOwnerView.as_view(), name="my_blog"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="detail"),
    path("create/", views.ArticleCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.ArticleUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.ArticleDeleteView.as_view(), name="delete"),
]
