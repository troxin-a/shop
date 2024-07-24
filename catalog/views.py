from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    CreateView,
    UpdateView,
)

from catalog.models import Category, Contacts, Product


class ProductCreateView(CreateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("catalog:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление товара"
        context["categories"] = Category.objects.all()
        return context


class ProductUpdateView(UpdateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("catalog:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование товара"
        context["categories"] = Category.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    template_name = "catalog/index.html"
    paginate_by = 8
    extra_context = {
        "title": "Аптека-лека ГЛАВНАЯ",
    }


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:index")


class ContactListView(ListView):
    model = Contacts
    template_name = "catalog/contacts.html"
    extra_context = {"title": "Обратная связь"}

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        text = request.POST.get("text")

        text_email = f"Имя: {name}\n" + f"Почта: {email}\n" + f"Текст письма: {text}"

        email = EmailMessage(
            subject="Письмо с обратной связи",
            body=text_email,
            from_email="anthonpashinov@yandex.ru",
            to=["anthonpashinov@yandex.ru"],
        )
        email.send(fail_silently=False)

        return redirect("catalog:index")
