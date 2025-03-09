from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from lms.models import Course, Lesson
from lms.validators import youtube_url_validator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class LessonSerializer(ModelSerializer):
    owner_email = SerializerMethodField()

    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            "video_url": {
                "validators": [youtube_url_validator]
            }  # Интеграция валидатора
        }

    def get_owner_email(self, obj):
        return obj.owner.email


class CourseSerializer(ModelSerializer):
    owner_email = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_owner_email(self, obj):
        return obj.owner.email

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.subscribers.filter(user=user).exists()
        return False


class CourseDetailSerializer(ModelSerializer):
    count_lessons_in_course = SerializerMethodField()
    lessons = SerializerMethodField()
    owner_email = SerializerMethodField()
    is_subscribed = SerializerMethodField()

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
