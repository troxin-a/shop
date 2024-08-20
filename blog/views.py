from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import ArticleModelForm
from blog.models import Article
from blog.utils import generate_slug, send_congratulation
from catalog.views import CustomLoginRequiredMixin


class ArticleListView(ListView):
    """Список статей"""

    model = Article
    paginate_by = 5
    extra_context = {"title": "Блог"}

    def get_queryset(self):
        """
        Только опубликованные статьи для всех
        Все статьи - для модератора
        """
        gueryset = super().get_queryset()
        if self.request.user.has_perm("blog.change_article"):
            return gueryset
        return gueryset.filter(is_published=True)


class ArticleListOwnerView(ListView):
    """Список статей владельца"""

    model = Article
    paginate_by = 5
    extra_context = {"title": "Мои статьи"}

    def get_queryset(self):
        """Только статьи владельца"""
        return super().get_queryset().filter(owner=self.request.user)


class ArticleDetailView(DetailView):
    """Просмотр статьи"""

    model = Article

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()

        if obj.views_count == 100:
            send_congratulation(obj)

        return obj


class ArticleCreateView(CustomLoginRequiredMixin, CreateView):
    """Создание статьи"""

    model = Article
    form_class = ArticleModelForm
    success_url = reverse_lazy("blog:my_blog")
    extra_context = {"title": "Добавление статьи"}

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()

            # Генерация слага
            new_article.slug = generate_slug(Article, new_article.title)

            # Назначение владельца
            new_article.owner = self.request.user

            # Заполнение даты публикации при нажатии соответствующего флага
            if new_article.is_published:
                new_article.published_at = datetime.now()
            else:
                new_article.published_at = None

            new_article.save()

        return super().form_valid(form)


class ArticleUpdateView(CustomLoginRequiredMixin, UpdateView):
    """Редактирование статьи"""

    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменение статьи"
        return context

    def get_form_class(self):
        if self.object.owner == self.request.user or self.request.user.has_perm(
            "blog.change_article"
        ):
            return ArticleModelForm
        raise PermissionDenied

    def form_valid(self, form):
        if form.is_valid():
            old_article = form.save()

            if old_article.is_published:
                old_article.published_at = datetime.now()
            else:
                old_article.published_at = None

            old_article.save()

        return super().form_valid(form)

    def get_success_url(self):
        # return reverse("blog:detail", args=(self.object.pk,))
        return reverse("blog:detail", args=[self.kwargs.get("pk")])


class ArticleDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление статьи"""

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm(
            "blog.delete_article"
        )

    model = Article
    success_url = reverse_lazy("blog:list")
