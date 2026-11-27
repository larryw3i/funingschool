import io
import re
import uuid
from datetime import date, datetime, timedelta
from decimal import (
    ROUND_DOWN,
    ROUND_FLOOR,
    ROUND_HALF_UP,
    Decimal,
    getcontext,
    localcontext,
)
from pathlib import Path
from urllib.parse import parse_qs, unquote

import numpy as np
import pandas as pd
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    IntegerField,
    Q,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce, TruncMonth
from django.http import HttpResponse, JsonResponse, QueryDict
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
from fnschool import _, fndate
from fnschool.local import get_local
from fnschool.views import (
    get_object_orders_from_cookie,
    get_search_params_from_cookie,
)

from .forms import StudentProfileForm, TeacherProfileForm
from .models import Course, StudentProfile, TeacherLeave, TeacherProfile
from .permissions import StudentRequiredMixin, TeacherRequiredMixin

# Create your views here.


@login_required
def edit_teacher_profile(request):
    if hasattr(request.user, "teacher_profile"):
        instance = request.user.teacher_profile
    else:
        instance = None

    if request.method == "POST":
        form = TeacherProfileForm(request.POST, instance=instance)
        next_url = request.POST.get("next")

        if form.is_valid():
            teacher_profile = form.save(commit=False)
            if not instance:
                teacher_profile.user = request.user
            teacher_profile.save()
            messages.success(request, _("Teacher profile saved successfully."))

            if next_url:
                return redirect(next_url)
            return redirect("education:list_teachers")
    else:
        form = TeacherProfileForm(instance=instance)
        next_url = request.GET.get("next", "")

    return render(
        request,
        "education/teacher_profile/edit.html",
        {
            "form": form,
            "user": request.user,
            "is_create": instance is None,
            "next": next_url,
        },
    )


@login_required
def edit_student_profile(request):
    if hasattr(request.user, "student_profile"):
        instance = request.user.student_profile
    else:
        instance = None

    if request.method == "POST":
        form = StudentProfileForm(request.POST, instance=instance)
        next_url = request.POST.get("next")

        if form.is_valid():
            student_profile = form.save(commit=False)
            if not instance:
                student_profile.user = request.user
            student_profile.save()
            messages.success(request, _("Student profile saved successfully."))

            if next_url:
                return redirect(next_url)
            return redirect("education:list_students")
    else:
        form = StudentProfileForm(instance=instance)
        next_url = request.GET.get("next", "")

    return render(
        request,
        "education/student_profile/edit.html",
        {
            "form": form,
            "user": request.user,
            "is_create": instance is None,
            "next": next_url,
        },
    )


class TeacherLeaveListView(TeacherRequiredMixin, ListView):
    model = TeacherLeave
    template_name = "education/teacher_leave/list.html"
    context_object_name = "teacher_leaves"

    paginate_by = 10
    paginate_orphans = 2

    def get_ordering(self):
        request = self.request
        self.ordering = get_object_orders_from_cookie(request, model=self.model)
        return self.ordering

    def paginate_queryset(self, queryset, page_size):
        search_params = get_search_params_from_cookie(self.request)
        page = int(search_params.get("page", 1))
        self.kwargs[self.page_kwarg] = page
        return super().paginate_queryset(queryset, page_size)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_paginate_by(self, queryset):
        search_params = get_search_params_from_cookie(self.request)
        page_size = int(search_params.get("page_size", self.paginate_by))
        self.paginate_by = page_size
        return self.paginate_by


class CourseListView(TeacherRequiredMixin, ListView):
    model = Course
    template_name = "education/course/list.html"
    context_object_name = "courses"

    paginate_by = 10
    paginate_orphans = 2

    def get_ordering(self):
        request = self.request
        self.ordering = get_object_orders_from_cookie(request, model=self.model)
        return self.ordering

    def paginate_queryset(self, queryset, page_size):
        search_params = get_search_params_from_cookie(self.request)
        page = int(search_params.get("page", 1))
        self.kwargs[self.page_kwarg] = page
        return super().paginate_queryset(queryset, page_size)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_paginate_by(self, queryset):
        search_params = get_search_params_from_cookie(self.request)
        page_size = int(search_params.get("page_size", self.paginate_by))
        self.paginate_by = page_size
        return self.paginate_by


class TeacherListView(TeacherRequiredMixin, ListView):
    model = StudentProfile
    template_name = "education/teacher_profile/list.html"
    context_object_name = "teachers"

    paginate_by = 10
    paginate_orphans = 2

    def get_ordering(self):
        request = self.request
        self.ordering = get_object_orders_from_cookie(request, model=self.model)
        return self.ordering

    def paginate_queryset(self, queryset, page_size):
        search_params = get_search_params_from_cookie(self.request)
        page = int(search_params.get("page", 1))
        self.kwargs[self.page_kwarg] = page
        return super().paginate_queryset(queryset, page_size)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_paginate_by(self, queryset):
        search_params = get_search_params_from_cookie(self.request)
        page_size = int(search_params.get("page_size", self.paginate_by))
        self.paginate_by = page_size
        return self.paginate_by


class StudentListView(StudentRequiredMixin, ListView):
    model = StudentProfile
    template_name = "education/student_profile/list.html"
    context_object_name = "students"

    paginate_by = 10
    paginate_orphans = 2

    def get_ordering(self):
        request = self.request
        self.ordering = get_object_orders_from_cookie(request, model=self.model)
        return self.ordering

    def paginate_queryset(self, queryset, page_size):
        search_params = get_search_params_from_cookie(self.request)
        page = int(search_params.get("page", 1))
        self.kwargs[self.page_kwarg] = page
        return super().paginate_queryset(queryset, page_size)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_paginate_by(self, queryset):
        search_params = get_search_params_from_cookie(self.request)
        page_size = int(search_params.get("page_size", self.paginate_by))
        self.paginate_by = page_size
        return self.paginate_by


# The end.
