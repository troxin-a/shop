from django import forms

from catalog.models import Product, Version


class ForbiddenWordsMixin:
    words = (
        "казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар"
    ).split(", ")

    def clean_forbidden_words(self, field: str):
        """
        Проверяет поле на запрещенные слова.
        Принимает на вход название поля
        """
        field_value = self.cleaned_data[field]

        for word in self.words:
            if word.lower() in field_value.lower():
                raise forms.ValidationError("Запрещенное слово")

        return field_value


class ProductForm(ForbiddenWordsMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "image",
            "price",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Подключаем стили к форме
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_name(self):
        """Валидация поля name"""
        return self.clean_forbidden_words("name")

    def clean_description(self):
        """Валидация поля description"""
        return self.clean_forbidden_words("description")


class VersionForm(ForbiddenWordsMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = [
            "product",
            "number",
            "name",
            "is_current",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Подключаем стили к форме
        for field in self.fields.values():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})
        # Скрываем поле product, т.к. оно должно быть заполнено автоматом
        self.fields["product"].widget = forms.HiddenInput()

    def clean_name(self):
        """Валидация поля name"""
        return self.clean_forbidden_words("name")

    def clean_is_current(self):
        """ Валидация поля is_current"""
        cleaned_data = self.cleaned_data["is_current"]

        # Получаем текущие версии конкретного продута.
        # И если среди них есть ТЕКУЩИЕ, вызываем исключение
        current_versions = Version.objects.filter(product=self.cleaned_data["product"], is_current=True)
        if cleaned_data and current_versions:
            raise forms.ValidationError(f"Текущая версия может быть только одна. На данный момент установлена текущей: версия {current_versions[0]}")

        return cleaned_data
