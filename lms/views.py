from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsModerator
from lms.permissions import IsOwner
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from lms.tasks import send_course_update_emails


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = [IsAdminUser]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAdminUser | IsModerator | IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        send_course_update_emails.delay(serializer.instance.id)  # Вызов задачи отправки писем

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if (
                self.request.user.is_superuser
                or self.request.user.groups.filter(name="Moderators").exists()
            ):
                return Course.objects.all()
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.none()  # Возвращаем пустой QuerySet для анонимных пользователей

class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if (
                self.request.user.is_superuser
                or self.request.user.groups.filter(name="Moderators").exists()
            ):
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=self.request.user)
        return (
            Lesson.objects.none()
        )  # Возвращаем пустой QuerySet для анонимных пользователей


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser | IsOwner]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if (
                self.request.user.is_superuser
                or self.request.user.groups.filter(name="Moderators").exists()
            ):
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=self.request.user)
        return (
            Lesson.objects.none()
        )  # Возвращаем пустой QuerySet для анонимных пользователей


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser | IsOwner]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if (
                self.request.user.is_superuser
                or self.request.user.groups.filter(name="Moderators").exists()
            ):
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=self.request.user)
        return (
            Lesson.objects.none()
        )  # Возвращаем пустой QuerySet для анонимных пользователей
