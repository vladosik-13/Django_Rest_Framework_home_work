from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lms.models import Course, Lesson

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(ModelSerializer):
    count_lessons_in_course = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return course.lesson_set.count()

    def get_lessons(self, course):
        lessons = course.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = ("title", "preview", "description", "count_lessons_in_course", "lessons")