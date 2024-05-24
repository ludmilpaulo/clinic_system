# signals.py

from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import send_order_email

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if instance.pk and 'status' in instance.get_dirty_fields():  # Ensure it's an update and status changed
        order_status_update_email = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Order Status Update</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 80%;
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #007BFF;
                }}
                p {{
                    line-height: 1.6;
                }}
                .order-details {{
                    margin: 20px 0;
                    padding: 10px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Hello {instance.user.username},</h1>
                <p>We wanted to let you know that the status of your order <strong>#{instance.id}</strong> has been updated to <strong>{instance.status}</strong>.</p>
                <div class="order-details">
                    <h2>Order Details:</h2>
                    <p><strong>Order ID:</strong> {instance.id}</p>
                    <p><strong>Status:</strong> {instance.status}</p>
                    <p><strong>Total Price:</strong> {instance.total_price} Kz</p>
                </div>
                <p>If you have any questions, feel free to <a href="mailto:support@example.com">contact our support team</a>.</p>
                <p>Thank you for shopping with us!</p>
                <div class="footer">
                    <p>&copy; {datetime.now().year} Your Company. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        send_order_email(
            subject='Order Status Update',
            html_content=order_status_update_email,
            recipient_list=[instance.user.email]
        )
