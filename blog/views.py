from datetime import datetime

from django.http import Http404
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


class ArticleListView(ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        object = super().get_object()
        object.views_count += 1
        object.save()

        if object.views_count == 22:
            send_congratulation(object)

        if not object.is_published:
            raise Http404("Статья не найдена или не опубликована")

        return object


class ArticleCreateView(CreateView):
    model = Article
    fields = "__all__"
    success_url = reverse_lazy("blog:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление статьи"
        return context

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = generate_slug(Article, new_article.title)

            if new_article.is_published:
                new_article.published_at = datetime.now()
            else:
                new_article.published_at = None

            new_article.save()

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
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


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("blog:list")
