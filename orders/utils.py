from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


# utils.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_order_pdf(order):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Order Confirmation for Order #{order.id}")
    p.drawString(100, 730, f"Total Price: {order.total_price} Kz")
    p.drawString(100, 710, f"Address: {order.address}, {order.city}, {order.postal_code}, {order.country}")
    p.drawString(100, 690, f"Payment Method: {order.payment_method}")

    p.drawString(100, 650, "Order Items:")
    height = 630
    for item in order.items.all():
        p.drawString(100, height, f"{item.quantity} x {item.drug.name} at {item.price} Kz each")
        height -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer.getvalue()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_order_email(subject, message, recipient_list, attachments=None):
    email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(message),
        from_email=settings.DEFAULT_FROM_EMAIL,  # Replace with your email or a configured email address
        to=recipient_list
    )
    email.attach_alternative(message, "text/html")
    if attachments:
        for attachment in attachments:
            email.attach(attachment['filename'], attachment['content'], attachment['mime_type'])
    email.send()


