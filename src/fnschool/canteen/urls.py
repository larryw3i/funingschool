from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "canteen"

urlpatterns = [
    path(
        "create_consumptions",
        views.create_consumptions,
        name="create_consumptions",
    ),
    path(
        "create_consumption/<int:ingredient_id>",
        views.create_consumptions,
        name="create_consumption",
    ),
    path(
        "delete_ingredient/<int:ingredient_id>",
        views.delete_ingredient,
        name="delete_ingredient",
    ),
    path(
        "edit_ingredient/<int:ingredient_id>",
        views.edit_ingredient,
        name="edit_ingredient",
    ),
    path(
        "list_ingredients",
        views.list_ingredients,
        name="list_ingredients",
    ),
    path(
        "create_consumptions",
        views.create_consumptions,
        name="create_consumptions",
    ),
    path(
        "create_ingredients",
        views.create_ingredients,
        name="create_ingredients",
    ),
    path(
        "get_template_workbook_of_purchased_ingredients",
        views.get_template_workbook_of_purchased_ingredients,
        name="get_template_workbook_of_purchased_ingredients",
    ),
]

# The end.
