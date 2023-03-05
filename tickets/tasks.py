from celery import shared_task
from tickets.emails import send_email_notification

@shared_task
def send_email(subject, message, from_user, to_user):
    """Function for sending async email for non blocking event."""
    send_email_notification(subject, message, from_user, to_user)


