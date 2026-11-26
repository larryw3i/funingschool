import re
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator

# students/models.py
# Create your models here.
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from fnprofile.models import Fnuser
from fnschool import _

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="as_student",
        null=True,
    )

    student_id = models.CharField(
        _("Student ID"),
        max_length=64,
        unique=True,
        help_text=_("Unique student identification number"),
    )
    grade = models.CharField(
        _("Grade"),
        max_length=32,
        help_text=_("Grade level, e.g. 2024"),
    )
    class_name = models.CharField(
        _("Class"),
        max_length=32,
        help_text=_("Class name, e.g. Class 3"),
    )

    enrollment_date = models.DateField(
        _("Enrollment Date"),
        blank=True,
        null=True,
        help_text=_("Date of enrollment"),
    )

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return f"{self.username} ({self.grade} {self.class_name})"


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="as_teacher",
        null=True,
    )

    teacher_certificate_number = models.CharField(
        _("Teacher Certificate Number"),
        max_length=64,
        unique=True,
        help_text=_("Teacher qualification certificate number"),
    )
    teacher_certificate_image = models.ImageField(
        _("Teacher Certificate Image"),
        upload_to="teacher_certificates/",
        blank=True,
        null=True,
        help_text=_("Upload teacher qualification certificate image"),
    )
    graduation_date = models.DateField(
        _("Graduation Date"),
        blank=True,
        null=True,
        help_text=_("Date of graduation"),
    )
    graduated_from = models.CharField(
        _("Graduated From"),
        max_length=512,
        blank=True,
        null=True,
        help_text=_("University or college graduated from"),
    )
    degree_certificate_number = models.CharField(
        _("Degree Certificate Number"),
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        help_text=_("Degree certificate serial number"),
    )
    degree_certificate_image = models.ImageField(
        _("Degree Certificate Image"),
        upload_to="degree_certificates/",
        blank=True,
        null=True,
        help_text=_("Upload degree certificate image"),
    )
    graduation_certificate_number = models.CharField(
        _("Graduation Certificate Number"),
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        help_text=_("Graduation certificate serial number"),
    )
    graduation_certificate_image = models.ImageField(
        _("Graduation Certificate Image"),
        upload_to="graduation_certificates/",
        blank=True,
        null=True,
        help_text=_("Upload graduation certificate image"),
    )
    major_category = models.CharField(
        _("Major Category"),
        max_length=128,
        blank=True,
        null=True,
        help_text=_("Broad major category, e.g. Science, Engineering"),
    )
    major_subcategory = models.CharField(
        _("Major Subcategory"),
        max_length=128,
        blank=True,
        null=True,
        help_text=_("Specific major, e.g. Computer Science"),
    )

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"


class Course(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name=_("Teacher"),
        related_name="courses",
        help_text=_("Teacher who teaches this course"),
    )
    grade = models.CharField(
        _("Grade"),
        max_length=32,
        help_text=_("Target grade level, e.g. 2024"),
    )
    subject = models.CharField(
        _("Subject"),
        max_length=128,
        help_text=_("Subject name, e.g. Mathematics, Chinese"),
    )
    topic = models.CharField(
        _("Topic"),
        max_length=256,
        help_text=_("Lesson topic or title"),
    )
    lesson_plan_file = models.FileField(
        _("Lesson Plan File"),
        upload_to="lesson_plans/%Y/%m/",
        blank=True,
        null=True,
        help_text=_("Upload lesson plan file (PDF, Word, etc.)"),
    )
    presentation_file = models.FileField(
        _("Presentation File"),
        upload_to="presentations/%Y/%m/",
        blank=True,
        null=True,
        help_text=_("Upload presentation file (PPT, PDF, etc.)"),
    )
    teaching_material_file = models.FileField(
        _("Teaching Material File"),
        upload_to="teaching_materials/%Y/%m/",
        blank=True,
        null=True,
        help_text=_("Upload other teaching materials"),
    )

    created_at = models.DateTimeField(
        null=True, auto_now_add=True, verbose_name=_("Time of creating.")
    )

    updated_at = models.DateTimeField(
        null=True, auto_now=True, verbose_name=_("Time of updating.")
    )

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.subject} - {self.topic} ({self.grade})"


class Leave(models.Model):
    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name=_("Teacher"),
        related_name="leaves",
        help_text=_("Teacher requesting leave"),
    )
    start_time = models.DateTimeField(
        _("Start Time"),
        help_text=_("Leave start date and time"),
    )
    end_time = models.DateTimeField(
        _("End Time"),
        help_text=_("Leave end date and time"),
    )
    reason = models.TextField(
        _("Reason"),
        help_text=_("Reason for leave"),
    )
    approver = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        verbose_name=_("Approver"),
        related_name="approved_leaves",
        blank=True,
        null=True,
        help_text=_("Teacher who approves this leave"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text=_("Leave approval status"),
    )
    remark = models.TextField(
        _("Remark"),
        blank=True,
        null=True,
        help_text=_("Additional remarks or notes"),
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("Leave")
        verbose_name_plural = _("Leaves")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.teacher} - {self.start_time.date()} to {self.end_time.date()}"


# The end.
