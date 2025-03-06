from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson
from .models import Subscription
from django.contrib.auth.models import Group

User = get_user_model()


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        self.moderator_user = User.objects.create_user(
            email="moderator@example.com", password="moderatorpassword"
        )
        self.regular_user = User.objects.create_user(
            email="user@example.com", password="userpassword"
        )
        self.another_user = User.objects.create_user(
            email="anotheruser@example.com", password="anotherpassword"
        )

        self.moderator_group = Group.objects.create(name="Moderators")
        self.moderator_user.groups.add(self.moderator_group)

        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.admin_user
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test Lesson Description",
            owner=self.admin_user,
        )

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("users:subscribe")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(
                user=self.regular_user, course=self.course
            ).exists()
        )

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.regular_user)
        Subscription.objects.create(user=self.regular_user, course=self.course)
        url = reverse("users:subscribe")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(
                user=self.regular_user, course=self.course
            ).exists()
        )

    def test_subscribe_with_invalid_course_id(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("users:subscribe")
        data = {"course_id": 999}  # Несуществующий ID курса
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(
            Subscription.objects.filter(user=self.regular_user, course_id=999).exists()
        )

    def test_subscribe_without_course_id(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("users:subscribe")
        data = {}  # Пустые данные
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.regular_user, course=self.course
            ).exists()
        )

    def test_subscribe_as_anonymous_user(self):
        url = reverse("users:subscribe")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.regular_user, course=self.course
            ).exists()
        )
