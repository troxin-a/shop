from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.forms import ProductForm, VersionForm
from catalog.models import Contacts, Product, Version


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Миксин запрещает url для анонимных пользователей
    перенаправляет на авторизацию
    """

    login_url = reverse_lazy("users:login")


class ProductCreateView(CustomLoginRequiredMixin, CreateView):
    """Создание продукта"""

    redirect_field_name = "redirect_to"
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")
    extra_context = {"title": "Новый товар"}

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save()
            obj.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(CustomLoginRequiredMixin, UpdateView):
    """Редактирование продукта"""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")
    extra_context = {"title": "Редактирование товара"}


class ProductListView(ListView):
    """Список продуктов (главная страница)"""

    model = Product
    template_name = "catalog/index.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Аптека-лека ГЛАВНАЯ"

        # Передаем в контест ТЕКУЩИЕ версии продуктов, расположенных
        # на странице пагинатора с оптимизацией запроса
        products = context_data["page_obj"]
        context_data["versions"] = Version.objects.filter(
            product__in=products, is_current=True
        ).select_related("product")

        return context_data


class ProductDetailView(DetailView):
    """Просмотр продукта"""

    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = self.object.name

        # Передаем в контест ВСЕ версии продукта с оптимизацией запроса
        product = context_data["object"]
        context_data["versions"] = Version.objects.filter(
            product=product
        ).select_related("product")
        return context_data


class ProductDeleteView(CustomLoginRequiredMixin, DeleteView):
    """Удаление продукта"""

    model = Product
    success_url = reverse_lazy("catalog:index")


class ContactListView(ListView):
    """Обратная связь с формой отправки письма"""

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


class VersionUpdateView(CustomLoginRequiredMixin, UpdateView):
    """Изменение одной из версий продукта"""

    model = Version
    form_class = VersionForm

    def get_success_url(self):
        # Переадрессация на товар после успешного редактирования версии
        return reverse("catalog:detail", args=[self.object.product_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование версии"
        return context


class VersionCreateView(CustomLoginRequiredMixin, CreateView):
    """Добавление версии продукта"""

    model = Version
    form_class = VersionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая версия"
        context["product_id"] = self.kwargs.get("pk")  # Для кнопки "Назад"
        return context

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     # Передача pk в инициализацию формы для
    #     # авто-заполнения продукта из адресной строки
    #     kwargs.update(initial = {"product": self.kwargs.get("pk")})
    #     return kwargs

    def get_initial(self):
        """Передача данных в форму"""
        initial = super().get_initial()
        # Автозаполнение продукта из адресной строки
        initial["product"] = self.kwargs.get("pk")
        return initial

    def get_success_url(self):
        # Переадрессация на товар после успешного создания версии
        return reverse("catalog:detail", args=[self.kwargs.get("pk")])


class VersionDeleteView(CustomLoginRequiredMixin, DeleteView):
    """Удаление версии продукта"""

    model = Version
    extra_context = {"title": "Удаление версии"}

    def get_success_url(self):
        # Переадрессация после успешного удаления на товар
        return reverse("catalog:detail", args=[self.object.product_id])
