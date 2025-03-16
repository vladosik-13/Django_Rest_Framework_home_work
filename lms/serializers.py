from rest_framework import serializers
from lms.models import Course, Lesson
from lms.validators import youtube_url_validator
from django.contrib.auth import get_user_model

User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            "video_url": {
                "validators": [youtube_url_validator]
            }
        }
        ref_name = 'LessonSerializer_LMS'  # Уникальное имя для сериализатора

    def get_owner_email(self, obj):
        return obj.owner.email

class CourseSerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        ref_name = 'CourseSerializer_LMS'  # Уникальное имя для сериализатора

    def get_owner_email(self, obj):
        return obj.owner.email

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.subscribers.filter(user=user).exists()
        return False

class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons_in_course = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "count_lessons_in_course",
            "lessons",
            "owner_email",
            "is_subscribed",
        )
        ref_name = 'CourseDetailSerializer_LMS'  # Уникальное имя для сериализатора

    def get_count_lessons_in_course(self, course):
        return course.lesson_set.count()

    def get_lessons(self, course):
        lessons = course.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    def get_owner_email(self, obj):
        return obj.owner.email

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.subscribers.filter(user=user).exists()
        return False