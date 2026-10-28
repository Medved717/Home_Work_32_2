from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from educations.models import Course, Lesson, Subscriptions
from educations.paginators import CoursePaginations, LessonPaginations
from educations.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionRequestSerializer,
    SubscriptionResponseSerializer,
)
from users.permissions import IsModer, IsOwner


@extend_schema(tags=["Course"])
@extend_schema_view(
    list=extend_schema(
        summary="Получение списка курсов.",
    ),
    update=extend_schema(
        summary="Изменение данных курса.",
    ),
    partial_update=extend_schema(
        summary="Частичное изменение данных курса.",
    ),
    create=extend_schema(
        summary="Создание нового курса",
    ),
    destroy=extend_schema(
        summary="Удаление курса",
    ),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginations

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAdminUser,)
        elif self.action == "partial_update":
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == "update":
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == "retrieve":
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == "list":
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == "destroy":
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


@extend_schema(tags=["Lesson"])
@extend_schema_view(get=extend_schema(summary="Получение списка уроков."))
class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginations


@extend_schema(tags=["Lesson"])
@extend_schema_view(post=extend_schema(summary="Создание урока."))
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdminUser | IsAuthenticated & ~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


@extend_schema(tags=["Lesson"])
@extend_schema_view(get=extend_schema(summary="Просмотр конкретного урока."))
class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsAdminUser | IsOwner,)


@extend_schema(tags=["Lesson"])
@extend_schema_view(put=extend_schema(summary="Изменение урока."),
                    patch=extend_schema(summary="Частичное изменение урока."))
class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsAdminUser | IsOwner,)


@extend_schema(tags=["Lesson"])
@extend_schema_view(delete=extend_schema(summary="Удаление урока."))
class LessonDestroyAPIViews(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAdminUser | IsOwner,)
    serializer_class = LessonSerializer


@extend_schema(tags=["Subscription"])
@extend_schema_view(
    post=extend_schema(
        summary="Создание и удаление подписки",
        request=SubscriptionRequestSerializer,
        responses={status.HTTP_200_OK: SubscriptionResponseSerializer},
    )
)
class SubscriptionsAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course = get_object_or_404(Course, pk=course_id)
        subscriptions = Subscriptions.objects.filter(user=user, course=course)

        if subscriptions.exists():
            subscriptions.delete()
            message = "Ваша подписка удалена"

        else:
            Subscriptions.objects.create(user=user, course=course)
            message = "Ваша подписка активирована"
        return Response({"message": message})
