import unittest
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson
from users.models import Subscription
from django.contrib.auth.models import Group

User = get_user_model()


class LessonCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_create_lesson_as_admin(self):
        self.client.login(email="admin@example.com", password="adminpassword")
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_as_moderator(self):
        self.client.login(email="moderator@example.com", password="moderatorpassword")
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_lesson_as_regular_user(self):
        self.client.login(email="user@example.com", password="userpassword")
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_lesson_as_anonymous_user(self):
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_update_lesson_as_admin(self):
        self.client.login(email="admin@example.com", password="adminpassword")
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_as_moderator(self):
        self.client.login(email="moderator@example.com", password="moderatorpassword")
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_as_owner(self):
        self.client.login(email="user@example.com", password="userpassword")
        self.lesson.owner = self.regular_user
        self.lesson.save()
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_as_non_owner(self):
        self.client.login(email="anotheruser@example.com", password="anotherpassword")
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.lesson.refresh_from_db()
        self.assertNotEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson_as_admin(self):
        self.client.login(email="admin@example.com", password="adminpassword")
        url = reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_as_moderator(self):
        self.client.login(email="moderator@example.com", password="moderatorpassword")
        url = reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_delete_lesson_as_owner(self):
        self.client.login(email="user@example.com", password="userpassword")
        self.lesson.owner = self.regular_user
        self.lesson.save()
        url = reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_as_non_owner(self):
        self.client.login(email="anotheruser@example.com", password="anotherpassword")
        url = reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_list_lessons(self):
        self.client.login(email="user@example.com", password="userpassword")
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_lesson(self):
        self.client.login(email="user@example.com", password="userpassword")
        url = reverse("lms:lesson_retrieve", kwargs={"pk": self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")
