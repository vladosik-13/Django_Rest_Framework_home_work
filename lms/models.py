from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="lms/course_preview", verbose_name="Превью курса"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        blank=True, null=True, help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="lms/lessons_preview", verbose_name="Превью урока"
    )
    video_url = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return f"{self.title} (курс: {self.course.title})"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
