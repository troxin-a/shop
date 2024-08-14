from datetime import datetime

from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Article
from blog.utils import generate_slug, send_congratulation
from catalog.views import CustomLoginRequiredMixin


class ArticleListView(ListView):
    """Список статей"""

    model = Article
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    """Просмотр статьи"""

    model = Article

    def get_object(self, queryset=None):
        object = super().get_object()
        object.views_count += 1
        object.save()

        if object.views_count == 100:
            send_congratulation(object)

        # if not object.is_published:
        #     raise Http404("Статья не найдена или не опубликована")

        return object


class ArticleCreateView(CustomLoginRequiredMixin, CreateView):
    """Создание статьи"""

    model = Article
    fields = "__all__"
    success_url = reverse_lazy("blog:list")
    extra_context = {"title": "Добавление статьи"}

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()

            # Генерация слага
            new_article.slug = generate_slug(Article, new_article.title)

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
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменение статьи"
        return context

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


class ArticleDeleteView(CustomLoginRequiredMixin, DeleteView):
    """Удаление статьи"""

    model = Article
    success_url = reverse_lazy("blog:list")
