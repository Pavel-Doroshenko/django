"""Формы для сайта"""
from dataclasses import dataclass

from django import forms
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from .models import Category, Husband, Women
# from prompt_toolkit.validation import ValidationError


@deconstructible
@dataclass
class RussianValidator:
    """Валидация по русским символам"""
    ALLOWED_CHARS = (
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    )
    code = "russian"

    def __init__(self, message=None):
        self.message = (
            message
            if message
            else "Должны присутствовать только русские символы, дефис и пробел."
        )

    def __call__(self, value):
        if not set(value) <= set(self.ALLOWED_CHARS):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class AddPostForm(forms.ModelForm):
    """Добавление поста в форму"""
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категории",
        empty_label="Категория не выбрана",
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        required=False,
        label="Муж",
        empty_label="Не замужем",
    )

    class Meta:
        model = Women
        fields = ["title", "slug", "content", "photo", "is_published", "cat", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 10}),
        }

    def clean_title(self):
        """Валидация заголовка"""
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длинна превышает 50 символов")

        return title


class UploadFileForm(forms.Form):
    """Загрузка файла"""
    file = forms.FileField(label="Файл")
