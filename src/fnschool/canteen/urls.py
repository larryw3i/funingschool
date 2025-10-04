from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "canteen"

urlpatterns = [
    path(
        "close_window",
        views.close_window,
        name="close_window",
    ),
    path(
        "update_category/<int:pk>",
        views.CategoryUpdateView.as_view(),
        name="update_category",
    ),
    path(
        "delete_category/<int:pk>",
        views.CategoryDeleteView.as_view(),
        name="delete_category",
    ),
    path(
        "create_category",
        views.CategoryCreateView.as_view(),
        name="create_category",
    ),
    path(
        "list_categories",
        views.CategoryListView.as_view(),
        name="list_categories",
    ),
    path(
        "new_consumption",
        views.new_consumption,
        name="new_consumption",
    ),
    path(
        "new_consumption/<int:consumption_id>",
        views.new_consumption,
        name="new_consumption",
    ),
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
