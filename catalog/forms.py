from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField
from catalog.models import Product, Version
from django import forms


class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = ["form-check-input"]
            else:
                field.widget.attrs["class"] = ["form-control"]


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["views_counter"]


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = "__all__"

    def clean_name(self):
        cleaned_data = self.cleaned_data.get("name")
        bad_list_name = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for bad_name in bad_list_name:
            if bad_name in cleaned_data:
                raise ValidationError(" Запрещенные слова недопустимы")
        return cleaned_data
