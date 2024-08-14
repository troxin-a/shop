import secrets
from django.contrib.auth import views
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, UpdateView


from users import forms
from users.models import User


class CustomLoginView(views.LoginView):
    """Авторизация"""

    form_class = forms.CustomAuthenticationForm
    template_name = "users/user_form.html"
    extra_context = {
        "title": "Авторизация",
        "btn_caption": "Войти",
        "password_reset1": "Восстановить пароль",
        "password_reset2": "Сгенерировать пароль автоматически",
    }


class UserCreateView(CreateView):
    """Регистрация"""

    model = User
    form_class = forms.CustomUserCreationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_created")
    extra_context = {
        "title": "Регистрация",
        "btn_caption": "Регистрация",
    }

    def form_valid(self, form):
        """Деактивация нового пользователя и отправка email для подтверждения"""
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.token = secrets.token_hex(8)
            user.save()

            host = self.request.get_host()
            url = f"http://{host}/users/confirm-email/{user.token}/"
            email = EmailMessage(
                subject="Подтверждение регистрации",
                body=f"Подтвердите регистрацию, перейдя по ссылке {url}",
                to=[user.email],
            )
            email.send(fail_silently=False)

        return super().form_valid(form)


def user_created(request):
    """Страница с инструкцией подтверждения после создания пользователя"""
    context = {
        "title": "Подтверждение email",
        "content": "Пожалуйста, подтвердите адрес электронной почты. Для этого необходимо перейти по ссылке в письме, отправленном на адрес",
    }
    return render(request, "users/user_form.html", context)


def confirm_email(request, token):
    """Подтверждение email и активация пользователя"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    return redirect(reverse("users:login"))


class ProfileView(UpdateView):
    """Редактирование профиля пользователя"""

    model = User
    form_class = forms.CustomUserChangeForm
    template_name = "users/user_form.html"
    extra_context = {
        "title": "Профиль",
        "btn_caption": "Сохранить",
        "change_pass": "Сменить пароль",
    }

    def get_object(self):
        """Возвращает пользователя для его редактирования"""
        return self.request.user

    def get_success_url(self) -> str:
        return reverse("users:profile")


class ResetPassView(FormView):
    """
    Автоматическая генерация пароля и отправка его на почту после ввода email.
    Первый вариант восстановления.
    """

    form_class = forms.ResetPassForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:password_reset_done")
    extra_context = {
        "title": "Генерация пароля",
        "btn_caption": "Отправить",
    }

    def form_valid(self, form):
        if form.is_valid:
            user = User.objects.get(email=form.cleaned_data["email"])
            password = get_random_string(12)
            user.set_password(password)
            user.save(update_fields=["password"])

            email = EmailMessage(
                subject="Генерация пароля",
                body=f"Ваш новый пароль {password}",
                to=[user.email],
            )
            email.send(fail_silently=False)

        return super().form_valid(form)


class CustomPasswordResetView(views.PasswordResetView):
    """
    Полный сброс пароля с последующим изменением (Ввод email).
    Второй вариант восстановления.
    """

    form_class = forms.CustomPasswordResetForm
    template_name = "users/user_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    extra_context = {
        "btn_caption": "Отправить",
    }


class CustomPasswordResetDoneView(views.PasswordResetDoneView):
    """Информационая страница об отправке письма для сброса пароля"""

    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(views.PasswordResetConfirmView):
    """Ввод нового пароля после сброса"""

    form_class = forms.CustomSetPasswordForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:password_reset_complete")
    extra_context = {
        "btn_caption": "Сохранить",
    }


class CustomPasswordResetCompleteView(views.PasswordResetCompleteView):
    """Информационная страница об успешном изменении пароля после сброса"""

    template_name = "users/password_reset_complete.html"


class CustomPasswordChangeView(views.PasswordChangeView):
    """Ручное изменение пароля"""

    form_class = forms.CustomPasswordChangeForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:password_change_done")
    extra_context = {
        "btn_caption": "Сохранить",
    }


class CustomPasswordChangeDoneView(views.PasswordChangeDoneView):
    """Информационная страница о ручном изменении пароля"""

    template_name = "users/user_form.html"
