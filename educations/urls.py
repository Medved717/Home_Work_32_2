from django.urls import path
from rest_framework.routers import SimpleRouter

from .apps import EducationsConfig
from .views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIViews,
                    LessonListAPIView, LessonRetrieveAPIView,
                    LessonUpdateAPIView, SubscriptionsAPIView)

app_name = EducationsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/list/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIViews.as_view(), name="lessons_delete",),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path('subscription/', SubscriptionsAPIView.as_view(), name='subscription'),
]

urlpatterns += router.urls
