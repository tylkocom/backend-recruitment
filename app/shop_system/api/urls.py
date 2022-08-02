from rest_framework import routers
from .view import CartViewSet, OrderViewSet, ShelfViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"carts", CartViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"shelf", ShelfViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
