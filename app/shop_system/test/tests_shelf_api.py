from django.contrib.auth.models import User
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop_system.models import Review, Shelf


class ShelfApiTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.normal_user = User.objects.create_user(
            username="user", password="userpass"
        )
        self.shelf = Shelf.objects.create(
            name="Test Furniture",
            description="Test Description",
            price=10.0,
        )
        self.review = Review.objects.create(
            description="Test review", rating=4, user=self.admin_user, shelf=self.shelf
        )
        self.review2 = Review.objects.create(
            description="Test review2",
            rating=3,
            user=self.normal_user,
            shelf=self.shelf,
        )

        self.detail_url = reverse("shelf-detail", kwargs={"pk": self.shelf.pk})
        self.list_url = reverse("shelf-list")

    def test_get_shelf(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.shelf.name)
        self.assertEqual(response.data["reviews_count"], 2)
        self.assertEqual(response.data["reviews_avg"], "3.50")
