from django import forms
from monitoring.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "product_type",
            "store",
            "sku",
            "regular_price",
            "promo_price",
            "promo_ends_at",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Назва продукту"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Опис продукту",
                    "rows": 4,
                }
            ),
            "product_type": forms.Select(attrs={"class": "form-select"}),
            "store": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Артикул (SKU)"}
            ),
            "regular_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "step": "0.01",
                }
            ),
            "promo_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00 (опціонально)",
                    "step": "0.01",
                }
            ),
            "promo_ends_at": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "YYYY-MM-DD",
                }
            ),
        }
        labels = {
            "name": "Назва",
            "description": "Опис",
            "product_type": "Тип продукту",
            "store": "Магазин",
            "sku": "Артикул (SKU)",
            "regular_price": "Звичайна ціна",
            "promo_price": "Акційна ціна",
            "promo_ends_at": "Дата закінчення акції",
        }
        help_texts = {
            "sku": "Унікальний ідентифікатор продукту",
            "promo_price": "Залиште порожнім, якщо немає акції",
            "promo_ends_at": "Дата у форматі YYYY-MM-DD",
        }
