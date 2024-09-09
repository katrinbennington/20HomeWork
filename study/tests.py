from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from study.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="not_moder@example.ru")
        self.course = Course.objects.create(name="test_name", description="test_description")
        self.lesson = Lesson.objects.create(name="test", course=self.course, owner=self.user,
                                            description="test_description")
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока"""
        url = reverse("study:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse("study:lesson-create")
        data = {
            "name": "test_new",
            "description": "test_description_new",
            "video": "https://www.youtube.com/watch?v=kV5oFbQ47UQ"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """Тестирование редактирования урока"""
        url = reverse("study:lesson-update", args=(self.lesson.pk,))
        data = {
            "name": "new_test",
            "description": "new_test_description",
            "video": "https://www.youtube.com/watch?v=kV5oFbQ47UQ"
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "new_test"
        )

    def test_lesson_delete(self):
        """Тестирование удаления урока"""
        url = reverse("study:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        """Тестирование просмотра списка уроков"""
        url = reverse("study:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": data["count"],
            "next": data["next"],
            "previous": data["previous"],
            "results": data["results"],
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="test", owner=self.user)
        self.is_sub = Subscription.objects.create(is_sub=False, user=self.user)

    def test_create_subscription(self):
        data = {
            "id": 2,
            "user": self.user.id,
            "course": self.course.id,
            "is_sub": False
        }

        result = {
            "id": data["id"],
            "user": data["user"],
            "course": data["course"],
            "is_sub": data["is_sub"]
        }

        response = self.client.post(reverse('study:subscription-list'), data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            data, result
        )
