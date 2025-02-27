from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Avg, Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..models import Cart, Order, Review, Shelf
from .serializer import (
    CartSerializer,
    OrderSerializer,
    ReviewCreateSerializer,
    ReviewInfoSerializer,
    ReviewSerializer,
    ShelfSerializer,
)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer

    def get_queryset(self):
        return Shelf.objects.annotate(
            reviews_avg=Avg("reviews__rating"), reviews_count=Count("reviews")
        )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"])
    def info(self, request):
        reviews = Review.objects.all()
        avg_rating = reviews.aggregate(average_rating=Avg("rating"))["average_rating"]
        if avg_rating is not None:
            avg_rating = Decimal(avg_rating).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        else:
            avg_rating = Decimal("0.00")

        serializer = ReviewInfoSerializer(
            {
                "review_count": reviews.count(),
                "review_average_rating": avg_rating,
            }
        )
        return Response(serializer.data)
