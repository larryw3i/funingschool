import calendar
import io
import re
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import DecimalField, ExpressionWrapper, F, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import escape_uri_path
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from fnschool import _, count_chinese_characters

from ..forms import (
    CategoryForm,
    ConsumptionForm,
    IngredientForm,
    PurchasedIngredientsWorkBookForm,
)
from ..models import Category, Consumption, Ingredient


def set_column_width_in_inches(worksheet, column, inches):
    char_width = inches * 96 / 7

    if isinstance(column, int):
        col_letter = get_column_letter(column)
    else:
        col_letter = column
    worksheet.column_dimensions[col_letter].width = char_width


def set_row_height_in_inches(worksheet, row, inches):
    points = inches * 72
    worksheet.row_dimensions[row].height = points


class CanteenWorkBook:
    def __init__(self, request, month):
        self.wb = Workbook()
        self.wb[self.wb.sheetnames[0]].sheet_state = "hidden"
        self.cover_sheet = self.wb.create_sheet(title=_("Sheet Cover"))
        self.storage_sheet = self.wb.create_sheet(title=_("Sheet Storage"))
        self.storage_list_sheet = self.wb.create_sheet(
            title=_("Sheet Storage List")
        )
        self.non_storage_sheet = self.wb.create_sheet(
            title=_("Sheet Non-Storage")
        )
        self.non_storage_list_sheet = self.wb.create_sheet(
            title=_("Sheet Non-Storage List")
        )
        self.consumption_sheet = self.wb.create_sheet(
            title=_("Sheet Consumption")
        )
        self.consumption_list_sheet = self.wb.create_sheet(
            title=_("Sheet Consumption List")
        )
        self.surplus_sheet = self.wb.create_sheet(title=_("Sheet Surplus"))
        self.center_alignment = Alignment(
            horizontal="center", vertical="center"
        )
        self.thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )
        self.font_16_bold = Font(size=16, bold=True)
        self.font_12 = Font(size=12)
        self.font_12_bold = Font(size=12, bold=True)

        self.request = request
        self.year = int(month.split("-")[0])
        self.month = int(month.split("-")[1])
        self.date_start = datetime(self.year, self.month, 1).date()
        self.date_end = datetime(
            self.year, self.month, calendar.monthrange(self.year, self.month)[1]
        ).date()

    def fill_in_cover_sheet(self):
        sheet = self.cover_sheet
        user = self.request.user
        title_cell = sheet.cell(1, 1)
        title_cell.value = _(
            "Table of {affiliation} Canteen Ingredients Procurement Statistics in {month:0>2} {year}"
        ).format(
            affiliation=user.affiliation,
            year=self.year,
            month=self.month,
        )
        title_cell.font = self.font_16_bold
        title_cell.alignment = self.center_alignment
        for col_num, width in [
            [1, 1.96],
            [2, 2.26],
            [3, 4.44],
        ]:
            set_column_width_in_inches(sheet, col_num, width)
        sheet.merge_cells("A1:C1")

        header_category_cell = sheet.cell(2, 1)
        header_category_cell.font = self.font_12_bold
        header_category_cell.value = _("Ingredient Categories (cover sheet)")
        header_category_cell.alignment = self.center_alignment
        header_category_cell.border = self.thin_border

        header_total_price_cell = sheet.cell(2, 2)
        header_total_price_cell.font = self.font_12_bold
        header_total_price_cell.value = _("Ingredient Total Prices")
        header_total_price_cell.alignment = self.center_alignment
        header_total_price_cell.border = self.thin_border

        header_note_cell = sheet.cell(2, 3)
        header_note_cell.font = self.font_12_bold
        header_note_cell.value = _("Procurement Note")
        header_note_cell.alignment = self.center_alignment
        header_note_cell.border = self.thin_border

        categories = Category.objects.filter(
            Q(user=user) & Q(is_disabled=False)
        ).all()

        set_row_height_in_inches(sheet, 2, 0.44)
        set_row_height_in_inches(sheet, 1, 0.60)

        for index, category in enumerate(categories):

            set_row_height_in_inches(sheet, 3 + index, 0.44)

            category_cell = sheet.cell(3 + index, 1)
            category_cell.value = category.name

            ingredients = Ingredient.objects.filter(
                Q(user=user)
                & Q(category=category)
                & Q(storage_date__gte=self.date_start)
                & Q(storage_date__lte=self.date_end)
                & Q(is_disabled=False)
            ).all()
            total_price_cell = sheet.cell(3 + index, 2)
            total_price_cell.value = sum([i.total_price for i in ingredients])

            note_cell = sheet.cell(3 + index, 3)
            note_cell.value = _(
                "Total price of storaged ingredients is {0}, total price of non-storaged ingredients is {1}."
            ).format(
                sum([i.total_price for i in ingredients if not i.is_ignorable]),
                sum([i.total_price for i in ingredients if i.is_ignorable]),
            )

            for cell in [category_cell, total_price_cell, note_cell]:
                cell.font = self.font_12
                cell.alignment = self.center_alignment
                cell.border = self.thin_border

        ingredients = Ingredient.objects.filter(
            Q(user=user)
            & Q(storage_date__gte=self.date_start)
            & Q(storage_date__lte=self.date_end)
            & Q(is_disabled=False)
        ).all()

        summary_row_num = len(categories) + 3
        summary_index_cell = sheet.cell(summary_row_num, 1)
        summary_index_cell.value = _("Procurement Summary")

        summary_total_price_cell = sheet.cell(summary_row_num, 2)
        summary_total_price_cell.value = sum(
            [i.total_price for i in ingredients]
        )

        summary_note_cell = sheet.cell(summary_row_num, 3)
        summary_note_cell.value = _(
            "Total price of storaged ingredients is {0}, total price of non-storaged ingredients is {1}."
        ).format(
            sum([i.total_price for i in ingredients if not i.is_ignorable]),
            sum([i.total_price for i in ingredients if i.is_ignorable]),
        )

        for cell in [
            summary_index_cell,
            summary_total_price_cell,
            summary_note_cell,
        ]:
            cell.font = self.font_12_bold
            cell.alignment = self.center_alignment
            cell.border = self.thin_border

        set_row_height_in_inches(sheet, len(categories) + 2, 0.44)

    def fill_in(self):
        self.fill_in_cover_sheet()
        # self.fill_in_storage_sheet()
        # self.fill_in_storage_list_sheet()
        # self.fill_in_non_storage_sheet()
        # self.fill_in_non_storage_list_sheet()
        # self.fill_in_consumption_sheet()
        # self.fill_in_consumption_list_sheet()
        # self.fill_in_surplus_sheet()
        # self.fill_in_food_sheets()

        return self.wb


def get_workbook(request, month):
    wb = CanteenWorkBook(request, month).fill_in()
    return wb
