from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Cart, Order, Review, Shelf
from .serializer import (
    CartSerializer,
    OrderSerializer,
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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False)
    def info(self, request):
        reviews = Review.objects.all()

        serializer = ReviewInfoSerializer(
            {
                "review_count": reviews.count(),
                "review_average_rating": reviews.aggregate(
                    average_rating=Avg("rating")
                )["average_rating"],
            }
        )
        return Response(serializer.data)
