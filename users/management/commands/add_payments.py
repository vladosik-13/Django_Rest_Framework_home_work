from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import Payment, User
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = "Добавляет тестовые платежи в базу данных"

    def handle(self, *args, **kwargs):
        # Получаем первого и последнего пользователя
        user1 = User.objects.first()
        user2 = User.objects.last()

        # Получаем первый курс и первый урок
        course1 = Course.objects.first()
        lesson1 = Lesson.objects.first()

        # Проверяем, существуют ли необходимые объекты
        if not user1:
            self.stdout.write(self.style.ERROR("Не найден первый пользователь"))
            return

        if not user2:
            self.stdout.write(self.style.ERROR("Не найден последний пользователь"))
            return

        if not course1:
            self.stdout.write(self.style.ERROR("Не найден первый курс"))
            return

        if not lesson1:
            self.stdout.write(self.style.ERROR("Не найден первый урок"))
            return

        Payment.objects.create(
            user=user1,
            payment_date=timezone.now(),
            course=course1,
            lesson=None,
            amount=1500.00,
            payment_method="transfer",
        )

        Payment.objects.create(
            user=user2,
            payment_date=timezone.now(),
            course=None,
            lesson=lesson1,
            amount=500.00,
            payment_method="cash",
        )

        self.stdout.write(self.style.SUCCESS("Тестовые платежи успешно добавлены"))
