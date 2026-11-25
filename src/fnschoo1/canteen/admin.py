# canteen/admin.py
from django.contrib import admin
from .models import CanteenManager


@admin.register(CanteenManager)
class CanteenManagerAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "full_name",
        "phone",
        "email",
        "affiliation",
        "superior_department",
        "date_of_birth",
        "address",
    ]
    search_fields = [
        "fnuser_ptr__username",
        "fnuser_ptr__first_name",
        "fnuser_ptr__last_name",
        "fnuser_ptr__email",
        "affiliation",
    ]
    list_filter = ["affiliation"]

    def username(self, obj):
        return obj.username

    def phone(self, obj):
        return obj.phone

    def email(self, obj):
        return obj.email

    def date_of_birth(self, obj):
        return obj.date_of_birth

    def address(self, obj):
        return obj.address


# The end.
