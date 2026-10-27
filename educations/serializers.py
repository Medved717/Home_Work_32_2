from django.core.serializers import serialize
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from educations.models import Course, Lesson
from educations.validators import InvalidLinkValidator


class LessonSerializer(ModelSerializer):


    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [InvalidLinkValidator('link_on_video')]


class CourseSerializer(ModelSerializer):
    count_lesson = SerializerMethodField()
    lessons_list = LessonSerializer(source='lessons', read_only=True, many=True)
    subscriptions = SerializerMethodField(read_only=True)

    def get_count_lesson(self, instance):
        return instance.lessons.count()

    def get_subscriptions(self, instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return instance.subscriptions_user.filter(user=user).exists()


    class Meta:
        model = Course
        fields = "__all__"
