from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_update_emails(course_id):
    from lms.models import Subscription, Course
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)
    subject = f'Обновление курса "{course.title}"'
    message = f'Курс "{course.title}" был обновлен. Проверьте новые материалы.'
    from_email = 'no-reply@example.com'
    recipient_list = [subscriber.user.email for subscriber in subscribers]

    send_mail(subject, message, from_email, recipient_list)