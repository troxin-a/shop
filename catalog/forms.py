from django import forms

from catalog.models import Product, Version


class ForbiddenWordsMixin:
    words = (
        "казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар"
    ).split(", ")

    def clean_forbidden_words(self, field: str):
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
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_name(self):
        return self.clean_forbidden_words("name")

    def clean_description(self):
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
        for field in self.fields.values():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})
        self.fields["product"].widget = forms.HiddenInput()

    def clean_name(self):
        return self.clean_forbidden_words("name")

    def clean_is_current(self):
        cleaned_data = self.cleaned_data["is_current"]
        current_versions = Version.objects.filter(product=self.cleaned_data["product"], is_current=True)

        if cleaned_data and current_versions:
            raise forms.ValidationError(f"Текущая версия может быть только одна. На данный момент установлена текущей: версия {current_versions[0]}")

        return cleaned_data
