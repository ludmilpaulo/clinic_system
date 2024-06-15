from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

def send_order_email(subject, message, recipient_list, attachments=None):
    email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(message),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list
    )
    email.attach_alternative(message, "text/html")
    if attachments:
        for attachment in attachments:
            email.attach(attachment['filename'], attachment['content'], attachment['mime_type'])
    email.send()
