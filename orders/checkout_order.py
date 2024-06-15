from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .utils import send_order_email
from .pdf import generate_order_pdf  # Correct import for generate_order_pdf
from django.contrib.auth.models import User
from pharmacy.models import Drug
from clinic_system.settings import MEDIA_ROOT
import os

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def checkout(request):
    data = request.data
    print("Request data:", data)

    token_key = data.get('token', None)
    print("Token key:", token_key)
    user = None
    new_user = False

    if token_key:
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            print("User retrieved from token:", user)
        except Token.DoesNotExist:
            print("Token does not exist.")

    if not user:
        user_id = data.get('user_id', None)
        print("User ID:", user_id)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                print("User retrieved from user_id:", user)
            except User.DoesNotExist:
                print("User does not exist for user_id:", user_id)

    if not user:
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
            print("Existing user retrieved:", user)
        except User.DoesNotExist:
            name = data.get('name', 'user')
            email = data.get('email', f'{name}@example.com')
            password = data.get('password', email)
            username = f'{name[0]}{User.objects.count() + 1}'
            print("Creating new user with username:", username)
            user = User.objects.create_user(username=username, email=email, password=password)
            new_user = True
            print("New user created:", user)

            token = Token.objects.create(user=user)
            token_key = token.key
            print("Token created for new user:", token_key)

    try:
        with transaction.atomic():
            print("Creating Order object...")
            order = Order.objects.create(
                user=user,
                total_price=data['total_price'],
                address=data['address'],
                city=data['city'],
                postal_code=data['postal_code'],
                country=data['country'],
                payment_method=data['payment_method']
            )
            print("Order object created:", order)

            for item in data['items']:
                drug = Drug.objects.get(id=item['id'])
                if drug.quantity_available < item['quantity']:
                    raise ValueError(f"Not enough stock for {drug.name}")
                print("Creating OrderItem object for drug:", drug)

                OrderItem.objects.create(
                    order=order,
                    drug=drug,
                    quantity=item['quantity'],
                    price=drug.price
                )
                print("OrderItem object created for drug:", drug.name)
                drug.quantity_available -= item['quantity']
                drug.save()
                print("Drug quantity updated for:", drug.name)

            pdf_content = generate_order_pdf(order, request)  # Pass the request object here
            if pdf_content is None:
                return Response({'detail': 'Error generating PDF.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            pdf_path = os.path.join(MEDIA_ROOT, 'invoices', f'order_{order.id}.pdf')
            print(f"PDF path: {pdf_path}")

            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_content)
            order.invoice = f'invoices/order_{order.id}.pdf'
            order.save(update_fields=['invoice'])
            print("Invoice saved:", order.invoice)

            order_confirmation_email = render_to_string('order_confirmation_email.html', {
                'user': user,
                'order': order,
                'year': now().year
            })

            attachments = [{
                'filename': f'order_{order.id}.pdf',
                'content': pdf_content,
                'mime_type': 'application/pdf',
            }]

            if new_user:
                account_details_email = render_to_string('account_details_email.html', {
                    'user': user,
                    'year': now().year
                })
                send_order_email(
                    subject='Your New Account Details',
                    message=account_details_email,
                    recipient_list=[user.email],
                    attachments=attachments
                )
                print("Account details email sent to:", user.email)

            send_order_email(
                subject='Order Confirmation',
                message=order_confirmation_email,
                recipient_list=[user.email],
                attachments=attachments
            )
            print("Order confirmation email sent to:", user.email)

            serializer = OrderSerializer(order)
            print("Order serialized successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError as ve:
        print("ValueError:", ve)
        return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Exception:", e)
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
