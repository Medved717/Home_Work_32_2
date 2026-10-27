from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from educations.models import Course, Lesson, Subscriptions
from educations.paginators import CoursePaginations, LessonPaginations
from educations.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginations

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAdminUser,)
        elif self.action == 'update':
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == 'list':
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == 'destroy':
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginations


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdminUser | IsAuthenticated & ~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsAdminUser | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsAdminUser | IsOwner,)


class LessonDestroyAPIViews(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAdminUser | IsOwner,)
    serializer_class = LessonSerializer


class SubscriptionsAPIView(APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        subscriptions = Subscriptions.objects.filter(user=user, course=course)

        if subscriptions.exists():
            subscriptions.delete()
            message = 'Ваша подписка удалена'

        else:
            Subscriptions.objects.create(user=user, course=course)
            message = 'Ваша подписка активирована'
        return Response({'message': message})

