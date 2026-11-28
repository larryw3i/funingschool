from datetime import date, datetime

from django import forms
from django.db.models import CheckConstraint, Q, Sum
from fnschool import _

from .models import Course, StudentProfile, TeacherLeave, TeacherProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["user", "created_at", "updated_at"]:
            self.fields.pop(field_name)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["user", "created_at", "updated_at"]:
            self.fields.pop(field_name)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class CourseForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["teacher_profile", "created_at", "updated_at"]:
            self.fields.pop(field_name)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TeacherLeaveCreateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in [
            "teacher_profile",
            "status",
            "created_at",
            "updated_at",
        ]:
            self.fields.pop(field_name)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TeacherLeaveReviewForm(forms.ModelForm):
    class Meta:
        model = TeacherLeave
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name in ["status", "remark"]:
                self.fields[field_name].widget.attrs.update(
                    {"class": "form-control"}
                )
            else:
                self.fields[field_name].disabled = True
                self.fields[field_name].widget.attrs.update(
                    {"class": "form-control", "readonly": True}
                )


class TeacherTrainingForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("user")
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# The end.
