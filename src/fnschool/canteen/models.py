from fnschool import _
from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Ingredient(models.Model):

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name=_("User"),
    )
    storage_date = models.DateField(verbose_name=_("Storage Date"))
    name = models.CharField(max_length=100, verbose_name=_("Ingredient Name"))
    meal_type = models.CharField(max_length=50, verbose_name=_("Meal Type"))
    category = models.CharField(max_length=50, verbose_name=_("Category"))
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Quantity")
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Total Price")
    )

    quantity_unit_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("Unit Name of Quantity"),
    )

    is_remaining = models.BooleanField(
        default=True, verbose_name=_("Is Remaining")
    )
    is_ignorable = models.BooleanField(
        default=False, verbose_name=_("Is Ignorable")
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = _("Ingredient List")

    def __str__(self):
        return f"{self.name} ({self.storage_date})"


class Consumption(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="consumptions",
        verbose_name=_("Ingredient"),
    )

    date_of_using = models.DateField(verbose_name=_("Date"))
    amount_used = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="消耗数量"
    )

    class Meta:
        verbose_name = _("Consumption Record")
        verbose_name_plural = _("Consumption Records")
        ordering = ["-date_of_using"]

    def __str__(self):
        return _("{0} of {1} was consumed on {2} .").format(
            str(self.amount_used) + self.ingredient.unit_name,
            self.ingredient.name,
            self.date_of_using,
        )


# The end.
