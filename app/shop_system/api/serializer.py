from rest_framework import serializers

from ..models import Cart, Order, Shelf


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ["name", "description", "price"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["products", "owner", "status"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["carts", "region", "order_date"]
