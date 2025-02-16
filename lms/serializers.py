from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lessons_in_course = SerializerMethodField()

    def get_count_lessons_in_course(self, lesson):
        return lesson.object.filter(course=lesson.course).count()

    class Meta:
        model = Course
        fields = ("title", "preview", "description", "count_lessons_in_course")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
