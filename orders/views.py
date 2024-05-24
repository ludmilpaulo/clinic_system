# views.py

from datetime import datetime
from pharmacy.models import Drug
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import  Order, OrderItem
from .serializers import OrderSerializer
from django.contrib.auth.models import User
from django.db import transaction
from .utils import send_order_email

@api_view(['POST'])
def checkout(request):
    user = request.user
    data = request.data

    try:
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                total_price=data['total_price'],
                address=data['address'],
                city=data['city'],
                postal_code=data['postal_code'],
                country=data['country'],
                payment_method=data['payment_method']
            )

            for item in data['items']:
                drug = Drug.objects.get(id=item['id'])
                if drug.quantity_available < item['quantity']:
                    raise ValueError(f"Not enough stock for {drug.name}")

                OrderItem.objects.create(
                    order=order,
                    drug=drug,
                    quantity=item['quantity'],
                    price=drug.price
                )
                # Reduce drug quantity
                drug.quantity_available -= item['quantity']
                drug.save()

            # Send order confirmation email
            order_confirmation_email = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Order Confirmation</title>
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
                    <h1>Thank you for your order, {user.username}!</h1>
                    <p>Your order # {order.id} has been received and is being processed.</p>
                    <div class="order-details">
                        <h2>Order Details:</h2>
                        <p><strong>Order ID:</strong> {order.id}</p>
                        <p><strong>Total Price:</strong> {order.total_price} Kz</p>
                    </div>
                    <p>If you have any questions, feel free to <a href="mailto:support@example.com">contact our support team</a>.</p>
                    <p>Thank you for shopping with us!</p>
                    <div class="footer">
                        <p>&copy; {datetime.now().year} Men's clinis. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            send_order_email(
                subject='Order Confirmation',
                html_content=order_confirmation_email,
                recipient_list=[user.email]
            )

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
