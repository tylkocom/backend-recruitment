from rest_framework import serializers

from ..models import Cart, Order, Review, Shelf


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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review


class ReviewInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    review_average_rating = serializers.DecimalField(
        max_digits=1, decimal_places=2, default=0
    )
