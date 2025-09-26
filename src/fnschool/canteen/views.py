import io
import pandas as pd
import numpy as np
from fnschool import count_chinese_characters
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from pathlib import Path
from fnschool import _
from django.http import HttpResponse
from openpyxl import Workbook
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import escape_uri_path
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Ingredient
from .forms import PurchasedIngredientsWorkBookForm, IngredientForm

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


def edit_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return render(
                request,
                "canteen/edit_ingredient_close.html",
            )
    else:
        form = IngredientForm(instance=ingredient)

    return render(request, "canteen/edit_ingredient.html", {"form": form})


def list_ingredients(request):
    search_query = request.GET.get("q", "")

    if search_query:
        ingredients = Ingredient.objects.filter(Q(name__icontains=search_query))
    else:
        ingredients = Ingredient.objects.all()

    per_page = request.GET.get("per_page")
    print(per_page)
    per_page = int(per_page) if str(per_page).isnumeric() else 10
    paginator = Paginator(ingredients, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    headers = [
        f.verbose_name
        for f in Ingredient._meta.fields
        if f.name not in ["id", "user"]
    ]
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "headers": headers,
        "per_page": per_page,
    }
    return render(request, "canteen/list_ingredients.html", context)


def create_ingredients(request):
    if request.method == "POST":
        form = PurchasedIngredientsWorkBookForm(request.POST, request.FILES)
        if form.is_valid():
            workbook_file = request.FILES["workbook_file"]

            if not workbook_file.name.endswith(".xlsx"):
                return HttpResponse(_('Please upload a file in "xlsx" format.'))

            df = pd.read_excel(workbook_file)

            for index, row in df.iterrows():
                Ingredient.objects.create(
                    user=request.user,
                    storage_date=row[storage_date_header[0]],
                    name=row[ingredient_name_header[0]],
                    meal_type=row[meal_type_header[0]],
                    category=row[category_header[0]],
                    quantity=row[quantity_header[0]],
                    total_price=row[total_price_header[0]],
                    quantity_unit_name=row[quantity_unit_name_header[0]],
                    is_ignorable=not row[is_ignorable_header[0]] == np.nan,
                )

            return redirect("canteen:list_ingredients")

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
        category_header,
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
    today = datetime.now().date()
    last_month = today + relativedelta(months=-1, day=1)
    filename = (
        _("Purchased Ingredients WorkBook ({0})").format(
            last_month.strftime("%Y%m")
        )
        + ".xlsx"
    )

    encoded_filename = escape_uri_path(filename)
    response["Content-Disposition"] = (
        f'attachment; filename="{encoded_filename}"'
    )

    return response


# The end.
