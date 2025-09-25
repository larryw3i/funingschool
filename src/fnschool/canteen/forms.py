from fnschool import _
from django import forms


class PurchasedIngredientsWorkBookForm(forms.Form):
    workbook_file = forms.FileField(
        label=_("Select a Spreadsheet File"),
        help_text=_("Office Open XML Spreadsheet only. (*.xlsx)"),
        widget=forms.ClearableFileInput(attrs={"accept": ".xlsx"}),
    )


# The end.
