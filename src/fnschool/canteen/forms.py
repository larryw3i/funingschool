from datetime import date, datetime
from fnschool import _
from django import forms

from .models import Ingredient


class PurchasedIngredientsWorkBookForm(forms.Form):
    workbook_file = forms.FileField(
        label=_("Select a Spreadsheet File"),
        help_text=_("Office Open XML Spreadsheet only. (*.xlsx)"),
        widget=forms.ClearableFileInput(attrs={"accept": ".xlsx"}),
    )


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            f.name
            for f in Ingredient._meta.fields
            if f.name not in ["id", "user"]
        ]

        current_year = date.today().year
        year_range = list(range(current_year - 100, current_year + 1))
        widgets = {
            "storage_date": forms.SelectDateWidget(
                years=year_range,
                attrs={"style": "width: 33.33%; display: inline-block;"},
            ),
        }


# The end.
