from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    owner_email = SerializerMethodField()

    class Meta:
        model = Lesson
        fields = "__all__"

    def get_owner_email(self, obj):
        return obj.owner.email


class CourseSerializer(ModelSerializer):
    owner_email = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_owner_email(self, obj):
        return obj.owner.email


class CourseDetailSerializer(ModelSerializer):
    count_lessons_in_course = SerializerMethodField()
    lessons = SerializerMethodField()
    owner_email = SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return course.lesson_set.count()

    def get_lessons(self, course):
        lessons = course.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    def get_owner_email(self, obj):
        return obj.owner.email

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
        )
