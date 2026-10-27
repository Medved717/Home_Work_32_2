from http.client import responses

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from educations.models import Course, Lesson, Subscriptions
from users.models import User


class CoursesTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.course_python = Course.objects.create(title='Python разработчик',
                                                   description='Курс по изучению языка программирования python.')
        self.course_C = Course.objects.create(title='C++ разработчик',
                                              description='Курс по изучению языка программирования C++.')

    def test_create_course(self):
        url = reverse('educations:courses-list')
        data = {
            'title': 'java разработчик',
            'description': 'Курс по изучению языка программирования java.'
        }
        response = self.client.post(url, data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.get(title='java разработчик').title, 'java разработчик')

    def test_list_course(self):
        url = reverse('educations:courses-list')
        response = self.client.get(url)
        self.assertEqual(response.data.get('count'), 2)

    def test_retrieve_course(self):
        url = reverse('educations:courses-detail', args=(self.course_python.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'Python разработчик')

    def test_update_course(self):
        url = reverse('educations:courses-detail', args=(self.course_C.pk,))
        data = {'title': 'Изменение'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'Изменение')

    def test_delete_course(self):
        url = reverse('educations:courses-detail', args=(self.course_C.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(Course.objects.get(title='Python разработчик').title, 'Python разработчик')


class LessonsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.course_python = Course.objects.create(title='Python разработчик',
                                                   description='Курс по изучению языка программирования python.')
        self.lesson_git = Lesson.objects.create(title='Git', description='Урок по основам git',
                                                course=self.course_python)
        self.lesson_dict = Lesson.objects.create(title='Dict', description='Словари в python')

    def test_create_lesson(self):
        url = reverse('educations:lessons_create')
        data = {
            'title': 'Урок списков',
            'description': 'Списки в языке программирования python'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.get(title='Урок списков').title, 'Урок списков')
        self.assertEqual(Lesson.objects.get(title='Урок списков').owner, self.user)

    def test_list_lesson(self):
        url = reverse('educations:lessons_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(response.data.get('count'), 2)

    def test_detail_lesson(self):
        url = reverse('educations:lessons_retrieve', args=(self.lesson_git.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(title='Git').title, 'Git')

    def test_update_lesson(self):
        url = reverse('educations:lessons_update', args=(self.lesson_git.pk,))
        data = {
            'title': 'Изменен'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(title='Изменен').title, 'Изменен')

    def test_delete_lesson(self):
        url = reverse('educations:lessons_delete', args=(self.lesson_git.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(Lesson.objects.get(title='Dict').title, 'Dict')

class ValidationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_invalid_link(self):
        url = reverse('educations:lessons_create')
        data = {
            'title': 'Урок списков',
            'description': 'Списки в языке программирования python',
            'link_on_video': 'http://vk.ru/video/1'
        }
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], 'Введена недопустимая ссылка!')

class SubscriptionsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Python разработчик',
                                                   description='Курс по изучению языка программирования python.')

    def test_subscription(self):
        url = reverse('educations:subscription')
        data = {
            'course_id': self.course.pk
        }

        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Subscriptions.objects.filter(user=self.user, course=self.course)),1)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Subscriptions.objects.filter(user=self.user, course=self.course)), 0)