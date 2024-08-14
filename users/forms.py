from django.contrib.auth import forms as user_forms
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from catalog.forms import StyleFormMixin
from users.models import User


class ExistsUserMixin:
    """Миксин для валидации email (поиск пользователя в базе)"""

    def clean_email(self):
        """При отсутствии пользователя с введенным email выводим исключение на форму"""
        data = self.cleaned_data.get("email")

        try:
            User.objects.get(email=data)
        except User.DoesNotExist:
            raise forms.ValidationError("Нет пользователя с такой почтой")

        return data


class CustomAuthenticationForm(StyleFormMixin, user_forms.AuthenticationForm):
    """Форма авторизации"""


class CustomPasswordResetForm(
    StyleFormMixin, ExistsUserMixin, user_forms.PasswordResetForm
):
    """Форма сброса пароля (ввод email)"""


class CustomSetPasswordForm(StyleFormMixin, user_forms.SetPasswordForm):
    """Форма заполнения пароля после сброса"""


class CustomPasswordChangeForm(StyleFormMixin, user_forms.PasswordChangeForm):
    """Форма ручного изменения пароля"""


class CustomUserCreationForm(StyleFormMixin, user_forms.UserCreationForm):
    """Форма создания нового пользователя"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class ResetPassForm(ExistsUserMixin, StyleFormMixin, forms.Form):
    """Форма автоматической генерации пароля"""

    email = forms.EmailField(
        label="Почта",
        help_text="Введите адрес электронной почты, указанной при регистрации",
    )


class CustomUserChangeForm(StyleFormMixin, user_forms.UserChangeForm):
    """Форма изменения профиля пользователя"""

    phone = PhoneNumberField(region="RU", label="Телефон", required=False)
    password = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "country",
            "phone",
            "avatar",
        )
