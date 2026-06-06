from datetime import date, datetime

from django import forms
from django.db.models import CheckConstraint, Q, Sum
from fnschool import _

from .models import Category, Consumption, Ingredient, MealType


class PurchasedIngredientsWorkBookForm(forms.Form):
    workbook_file = forms.FileField(
        label=_("Select a Spreadsheet File"),
        help_text=_("Office Open XML Spreadsheet only. (*.xlsx)"),
        widget=forms.ClearableFileInput(attrs={"accept": ".xlsx"}),
    )


class IngredientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Ingredient
        fields = [
            f.name
            for f in Ingredient._meta.fields
            if f.name not in ["id", "user", "updated_at", "created_at"]
        ]

        current_year = date.today().year
        year_range = list(range(current_year - 100, current_year + 1))
        widgets = {
            "storage_date": forms.SelectDateWidget(
                years=year_range,
                attrs={
                    "style": "width: 33.33%; display: inline-block;",
                },
            ),
        }

    def clean_storage_date(self):
        storage_date = self.cleaned_data.get("storage_date", None)
        ingredient = self.instance
        if not ingredient.consumptions.exists():
            return storage_date
        ingredient.consumptions.filter(date_of_using__lt=storage_date).delete()
        return storage_date

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        ingredient = self.instance
        if not ingredient.consumptions.exists():
            return quantity
            pass
        total_amount_used = (
            ingredient.consumptions.aggregate(
                total_amount_used=Sum("amount_used")
            )["total_amount_used"]
            or 0
        )
        if total_amount_used < quantity:
            return quantity
            pass
        deleted_amount_used_sum = 0
        for c in ingredient.consumptions.order_by("-date_of_using").all():
            deleted_amount_used_sum += c.amount_used
            c.delete()
            if total_amount_used - deleted_amount_used_sum <= quantity:
                break
                pass
            pass
        return quantity


class ConsumptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._is_disabled = False
        for name in self.fields:
            self.fields[name].label = ""
            self.fields[name].widget.attrs.update(
                {
                    "id": f"id_{name}_{self.instance.ingredient.id}",
                    "class": "form-control",
                }
            )

        self.fields["amount_used"].widget.attrs.update(
            {
                "title": _("Please enter a number."),
                "type": "number",
                "min": "0",
                "step": "1",
                "class": "form-control input-consumption-amount_used",
            }
        )

    class Meta:
        model = Consumption
        fields = "__all__"
        widgets = {
            "amount_used": forms.NumberInput(
                attrs={
                    "style": "width: 95px; text-align: center; font-family: Mono;"
                }
            ),
            "date_of_using": forms.HiddenInput(),
            "ingredient": forms.HiddenInput(),
        }

    @property
    def is_disabled(self):
        return self._is_disabled
        pass

    @is_disabled.setter
    def is_disabled(self, value):
        self._is_disabled = value
        if self._is_disabled:
            self.fields["amount_used"].disabled = True
            self.fields["amount_used"].widget.attrs.update(
                {
                    "readonly": "readonly",
                }
            )
        pass


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "abbreviation",
            "priority",
            "pin_to_consumptions_top",
            "is_disabled",
        ]
        widgets = {
            "priority": forms.NumberInput(
                attrs={
                    "title": _(
                        "Numbers with smaller values have higher priority."
                    ),
                },
            ),
        }


class MealTypeForm(forms.ModelForm):
    class Meta:
        model = MealType
        fields = ["name", "abbreviation", "is_disabled"]


# The end.
