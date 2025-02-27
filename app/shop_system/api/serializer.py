from django.db.models.query_utils import Q
from rest_framework import serializers

from ..models import Cart, Order, Review, Shelf


class ShelfSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    reviews_count = serializers.IntegerField()
    reviews_avg = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )

    class Meta:
        model = Shelf
        fields = [
            "name",
            "description",
            "price",
            "reviews",
            "reviews_count",
            "reviews_avg",
        ]

    def get_reviews(self, obj):
        return obj.reviews.values_list("rating", flat=True)


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
        fields = ["rating", "description", "shelf", "user"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["rating", "description", "shelf", "user"]

    def create(self, validated_data):

        buyer = validated_data.pop("user")
        reviewed_shelf = validated_data.pop("shelf")

        was_bought = reviewed_shelf.carts.filter(
            Q(owner=buyer) & Q(status=Cart.ORDERED)
        ).exists()

        if not was_bought:
            raise serializers.ValidationError("You need to buy a shelf first")

        already_reviewed = reviewed_shelf.reviews.filter(user=buyer).exists()

        if already_reviewed:
            raise serializers.ValidationError("You already reviewed this product")

        review = Review.objects.create(
            user=buyer, shelf=reviewed_shelf, **validated_data
        )

        return review


class ReviewInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    review_average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, default=0.0
    )
