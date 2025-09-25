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


# The end.
