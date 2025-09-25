import io
from fnschool import count_chinese_characters
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from pathlib import Path
from fnschool import _
from django.http import HttpResponse
from openpyxl import Workbook
from django.shortcuts import render
from django.utils.encoding import escape_uri_path

from .forms import PurchasedIngredientsWorkBookForm

# Create your views here.

storage_date_header = (
    _("Storage Date"),
    _(
        'Formats like "YYYY.mm.dd", "YYYY/mm/dd", '
        + '"YYYY.mm.dd", "mm/dd", "mmdd", and "mm.dd" '
        + "are all acceptable. In short, FNSCHOOL wants to be "
        + "compatible with all the formats you like, but if "
        + "something goes wrong, you have to tell the "
        + "developers. Thank you!"
    ),
)
ingredient_name_header = (_("Ingredient Name"), _("Name of Ingredient"))
meal_type_header = (
    _("Meal Type"),
    _(
        "For example, breakfast, dinner, regular meals, "
        + "nutritious meals, etc., when generating a spreadsheet,"
        + " each meal category corresponds to a spread sheet. "
        + "If left blank, only one spreadsheet will be generated."
    ),
)

category_header = (
    _("Category"),
    _(
        "Usually there are seven categories: vegetables, meat, "
        + "grains, seasonings, eggs and milk, oils, and fruits."
    ),
)
quantity_header = (
    _("Quantity"),
    _(
        "When you purchase ingredients, it's best not to have "
        + "decimals in the quantity, as this can "
        + "be a big hassle!"
    ),
)


total_price_header = (
    _("Total Price"),
    None,
)
quantity_unit_name_header = (
    _("Unit Name of Quantity"),
    None,
)
is_ignorable_header = (
    _("Is Ignorable"),
    _("As long as a cell has content, it will be considered " + 'as "yes".'),
)


def create_ingredients(request):
    if request.method == "POST":
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            workbook_file = request.FILES["workbook_file"]

            if not workbook_file.name.endswith(".xlsx"):
                return HttpResponse(_('Please upload a file in "xlsx" format.'))

            try:
                df = pd.read_excel(workbook_file)
                return render(
                    request,
                    "canteen/create_ingredients.html",
                    {"data": df.to_html(classes="table")},
                )
            except Exception as e:
                return HttpResponse(
                    f_("An error occurred while processing the file.")
                )
    else:
        form = PurchasedIngredientsWorkBookForm()
    return render(request, "canteen/create_ingredients.html", {"form": form})


def get_template_workbook_of_purchased_ingredients(request):
    global storage_date_header, ingredient_name_header, meal_type_header
    global quantity_header, quantity_unit_name_header, total_price_header
    global is_ignorable_header
    headers = [
        storage_date_header,
        ingredient_name_header,
        meal_type_header,
        quantity_header,
        quantity_unit_name_header,
        total_price_header,
        is_ignorable_header,
    ]

    wb = Workbook()
    ws = wb.active
    ws.title = _("Purchased Ingredients Sheet")

    for i, (h, c) in enumerate(headers):
        h_cell = ws.cell(1, i + 1)

        center_alignment = Alignment(horizontal="center", vertical="center")
        h_cell.alignment = center_alignment

        mono_font = Font(
            name="Mono",
            size=12,
        )
        h_cell.font = mono_font

        h_cell.value = h
        column_letter = get_column_letter(i + 1)
        hans_len = count_chinese_characters(h)
        hans_len = (hans_len + 2) if hans_len else hans_len
        ws.column_dimensions[column_letter].width = len(h) + hans_len + 2
        if c:
            h_cell.comment = Comment(c, _("the FNSCHOOL Authors"))

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type=(
            "application/"
            + "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
    filename = _("Purchased Ingredients WorkBook") + ".xlsx"

    encoded_filename = escape_uri_path(filename)
    response["Content-Disposition"] = (
        f'attachment; filename="{encoded_filename}"'
    )

    return response


# The end.
