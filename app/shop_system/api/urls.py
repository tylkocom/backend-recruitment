from django.urls import include, path
from rest_framework import routers

from .view import CartViewSet, OrderViewSet, ReviewViewSet, ShelfViewSet

router = routers.DefaultRouter()
router.register(r"carts", CartViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"shelf", ShelfViewSet)
router.register(r"review", ReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
