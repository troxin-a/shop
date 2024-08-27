from django.core.exceptions import PermissionDenied
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
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)

from catalog.forms import ProductForm, ProductFormModerator, VersionForm
from catalog.models import Category, Contacts, Product, Version
from catalog.services import (
    get_categories_from_cache,
    get_product_counts_by_category_from_cache,
    get_products_from_cache,
    get_version_from_cache,
)
from config.settings import EMAIL_ADMIN


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Миксин запрещает url для анонимных пользователей
    перенаправляет на авторизацию
    """

    login_url = reverse_lazy("users:login")


class ProductListMixin:
    model = Product
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        for product in context_data["page_obj"]:
            product.version = get_version_from_cache(product.pk)

        return context_data


class OwnerAccessMixin(UserPassesTestMixin):
    """Разрешение для владельца"""

    def test_func(self):
        product = Product.objects.get(pk=self.kwargs.get("pk"))
        return product.owner == self.request.user


class ProductCreateView(CustomLoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание продукта"""

    model = Product
    permission_required = "catalog.add_product"
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
    success_url = reverse_lazy("catalog:index")
    extra_context = {"title": "Редактирование товара"}

    def get_success_url(self) -> str:
        return reverse("catalog:detail", args=[self.object.pk])

    def get_form(self, form_class=None):
        """Если товар не опубликован, отключаем флаг публикации для модератора"""
        form = super().get_form(form_class)
        if (
            self.request.user.has_perms(
                [
                    "catalog.cancel_product_is_publish",
                    "catalog.can_change_product_description",
                    "catalog.can_change_product_category",
                ]
            )
            and not self.object.is_published
        ):
            form.fields["is_published"].disabled = True
            # del form.fields["is_published"]
        return form

    def get_form_class(self):
        """
        Если имеются права модератора, указываем форму модератора.
        Если это просто владелец товара, указываем полную форму товара
        В остальных случаях редактирование запрещено
        """
        if self.request.user.has_perms(
            [
                "catalog.cancel_product_is_publish",
                "catalog.can_change_product_description",
                "catalog.can_change_product_category",
            ]
        ):
            return ProductFormModerator
        elif self.request.user == self.object.owner:
            return ProductForm
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Дополнительная проверка на установку публикации.
        Модератор может снимать с публикации, но не публиковать!
        """
        if self.request.user.has_perm("catalog.cancel_product_is_publish"):
            obj = self.get_object()
            check_btn_is_publushed = True if request.POST.get("is_published") else False
            if not obj.is_published and check_btn_is_publushed:
                return redirect(reverse_lazy("catalog:index"))
        return super().post(request, *args, **kwargs)


class ProductListView(ProductListMixin, ListView):
    """Список продуктов (главная страница)"""

    template_name = "catalog/index.html"
    extra_context = {"title": "Аптека-лека ГЛАВНАЯ"}

    def get_queryset(self):
        """Только опубликованные продукты"""
        return get_products_from_cache()


class ProductListOwnerView(ProductListMixin, ListView):
    """Список продуктов продавца"""

    template_name = "catalog/product_list_owner.html"
    extra_context = {"title": "Мои продукты"}

    def get_queryset(self):
        """Только владелец может видеть свои продукты"""
        return super().get_queryset().filter(owner=self.request.user)


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


class ProductDeleteView(CustomLoginRequiredMixin, OwnerAccessMixin, DeleteView):
    """Удаление продукта"""

    model = Product
    success_url = reverse_lazy("catalog:index")


class CategoryListView(ListView):
    """Список категорий"""

    paginate_by = 50
    extra_context = {"title": "Категории"}

    def get_queryset(self):
        return get_categories_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем количество товаров для каждой категории
        for category in context["category_list"]:
            category.count = get_product_counts_by_category_from_cache(category)
        return context


class ProductByCategoryListView(ProductListMixin, ListView):
    """Список товаров по категориям"""

    template_name = "catalog/index.html"

    def get_queryset(self):
        """Только опубликованные продукты конкретной категории"""
        return get_products_from_cache(self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs.get("pk"))
        return context


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
            to=[EMAIL_ADMIN],
        )
        email.send(fail_silently=False)

        return redirect("catalog:index")


class VersionUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Изменение одной из версий продукта"""

    model = Version
    form_class = VersionForm

    def test_func(self):
        return self.get_object().product.owner == self.request.user

    def get_success_url(self):
        # Переадрессация на товар после успешного редактирования версии
        return reverse("catalog:detail", args=[self.object.product_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование версии"
        return context


class VersionCreateView(CustomLoginRequiredMixin, OwnerAccessMixin, CreateView):
    """Добавление версии продукта"""

    model = Version
    form_class = VersionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая версия"
        context["product_id"] = self.kwargs.get("pk")  # Для кнопки "Назад"
        return context

    def get_initial(self):
        """Передача данных в форму"""
        initial = super().get_initial()
        # Автозаполнение продукта из адресной строки
        initial["product"] = self.kwargs.get("pk")
        return initial

    def get_success_url(self):
        # Переадрессация на товар после успешного создания версии
        return reverse("catalog:detail", args=[self.kwargs.get("pk")])


class VersionDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление версии продукта"""

    model = Version
    extra_context = {"title": "Удаление версии"}

    def test_func(self):
        return self.get_object().product.owner == self.request.user

    def get_success_url(self):
        # Переадрессация после успешного удаления на товар
        return reverse("catalog:detail", args=[self.object.product_id])
