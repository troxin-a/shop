from django import forms

from blog.models import Article
from catalog.forms import StyleFormMixin


class ArticleModelForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "preview",
            "is_published",
        )
