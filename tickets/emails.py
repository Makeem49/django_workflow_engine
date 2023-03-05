from django.core.mail import send_mail


def send_email_notification(subject, message, from_user, to_user, fail_silently=False):
    """
    subject: Email subject,
    message: Email content
    from_user: The person sending thhe email,
    to_user: The personn receiving the email
    """

    send_mail(
        subject,
        message,
        from_user,
        [to_user],
        fail_silently=fail_silently,
    )
