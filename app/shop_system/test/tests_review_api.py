from django.contrib.auth.models import User
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop_system.models import Cart, Review, Shelf


class ReviewApiTestCase(APITestCase):
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

        self.detail_url = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.url = reverse("review-list")
        self.info_url = reverse("review-info")

    def test_get_reviews(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], self.review.description)
        self.assertEqual(response.data["rating"], 4)

    def test_get_info_reviews(self):
        response = self.client.get(self.info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 2)
        self.assertEqual(response.data["review_average_rating"], "3.50")

    def test_create_review_without_purchase(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "rating": 1,
            "description": "test1",
            "shelf": self.shelf.pk,
            "user": self.admin_user.id,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You need to buy a shelf first", str(response.data))

    def test_create_review_already_reviewed(self):
        self.client.force_authenticate(user=self.normal_user)
        self.cart = Cart.objects.create(status=Cart.ORDERED, owner=self.normal_user)
        self.cart.products.add(self.shelf)
        data = {
            "rating": 1,
            "description": "test1",
            "shelf": self.shelf.pk,
            "user": self.normal_user.id,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You already reviewed this product", str(response.data))
