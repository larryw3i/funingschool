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


class CanteenWorkBook:
    def __init__(self, request, month):
        self.wb = Workbook()
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

        self.request = request
        self.year = int(month.split("-")[0])
        self.month = int(month.split("-")[1])

    def fill_in_cover_sheet(self):
        sheet = self.cover_sheet
        user = self.request.user
        sheet.cell(
            1,
            1,
            _(
                "Table of {superior_department} Canteen Ingredients Procurement Statistics in {month:0>} {year}"
            ).format(
                superior_department=user.superior_department,
                year=self.year,
                month=self.month,
            ),
        )
        sheet.merge_cells("A1:C1")

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
