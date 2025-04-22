from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Lesson
from django.contrib.auth.models import Group

User = get_user_model()


class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            is_staff=True,
            is_superuser=True,
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

        # Добавляем урок, принадлежащий regular_user
        self.regular_user_lesson = Lesson.objects.create(
            course=self.course,
            title="Regular User Lesson",
            description="Regular User Lesson Description",
            owner=self.regular_user,
        )

        # Добавляем еще один урок, принадлежащий admin_user
        self.another_admin_lesson = Lesson.objects.create(
            course=self.course,
            title="Another Admin Lesson",
            description="Another Admin Lesson Description",
            owner=self.admin_user,
        )

    def test_create_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
            "owner": self.admin_user.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 4)

    def test_create_lesson_as_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
            "owner": self.moderator_user.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_create_lesson_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
            "owner": self.regular_user.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_create_lesson_as_anonymous_user(self):
        url = reverse("lms:lesson_create")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_update_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
            "owner": self.admin_user.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_as_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
            "owner": self.moderator_user.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.lesson.refresh_from_db()
        self.assertNotEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_as_owner(self):
        self.client.force_authenticate(user=self.regular_user)
        self.regular_user_lesson.owner = self.regular_user
        self.regular_user_lesson.save()
        url = reverse("lms:lesson_update", kwargs={"pk": self.regular_user_lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
            "owner": self.regular_user.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user_lesson.refresh_from_db()
        self.assertEqual(self.regular_user_lesson.title, "Updated Lesson")

    def test_update_lesson_as_non_owner(self):
        self.client.force_authenticate(user=self.another_user)
        url = reverse("lms:lesson_update", kwargs={"pk": self.regular_user_lesson.id})
        data = {
            "course": self.course.id,
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updatedlesson",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.regular_user_lesson.refresh_from_db()
        self.assertNotEqual(self.regular_user_lesson.title, "Updated Lesson")

    def test_delete_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_delete_lesson_as_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_delete_lesson_as_owner(self):
        self.client.force_authenticate(user=self.regular_user)
        self.regular_user_lesson.owner = self.regular_user
        self.regular_user_lesson.save()
        url = reverse("lms:lesson_delete", kwargs={"pk": self.regular_user_lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_delete_lesson_as_non_owner(self):
        self.client.force_authenticate(user=self.another_user)
        url = reverse("lms:lesson_delete", kwargs={"pk": self.regular_user_lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_lesson(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lesson_retrieve", kwargs={"pk": self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")
