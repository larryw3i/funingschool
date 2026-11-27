from datetime import date, datetime

from django import forms
from django.db.models import CheckConstraint, Q, Sum
from fnschool import _

from .models import (
        StudentProfile,
        TeacherProfile,
        Course,
        TeacherLeave
)

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("user")
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("user")
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# The end.
