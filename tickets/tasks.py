from celery import shared_task
from .emails import send_email_notification


@shared_task
def send_mail(subject, message, from_user, to_user):
    send_email_notification(subject, message, from_user, to_user)


