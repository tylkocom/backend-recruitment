from django.contrib.auth.models import User
from django.db import models


class Shelf(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=16)


class Cart(models.Model):
    CREATED = "CREATED"
    ORDERED = "ORDERED"
    STATUS = (
        (CREATED, "CREATED"),
        (ORDERED, "ORDERED"),
    )
    products = models.ManyToManyField(Shelf, related_name="carts")
    owner = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default=CREATED, max_length=7)


class Order(models.Model):
    UK = "UK"
    DE = "DE"
    FR = "FR"
    PL = "PL"
    NL = "NL"

    REGIONS = (
        (UK, "United Kingdom"),
        (DE, "Germany"),
        (FR, "France"),
        (PL, "Poland"),
        (NL, "Netherlands"),
    )

    carts = models.ForeignKey(Cart, related_name="orders", on_delete=models.CASCADE)
    region = models.CharField(choices=REGIONS, max_length=2)
    order_date = models.DateTimeField(auto_now_add=True)
