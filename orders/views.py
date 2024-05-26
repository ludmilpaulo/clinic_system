from datetime import datetime
from django.contrib.auth.models import User
from accounts.models import ConsultationCategory
from accounts.serializers import ConsultationCategorySerializer
from pharmacy.models import Drug, Image
from datetime import datetime
from django.contrib.auth.models import User
from pharmacy.models import Drug
from pharmacy.serializers import DrugSerializer, ImageSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from .utils import send_order_email, generate_order_pdf
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt


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
        # If user does not exist, create a new user
        name = data.get('name', 'user')
        email = data.get('email', f'{name}@example.com')
        password = data.get('password', email)  # Using email as password
        username = f'{name[0]}{User.objects.count() + 1}'  # Create a unique username using the first letter of the name
        print("Creating new user with username:", username)
        user = User.objects.create_user(username=username, email=email, password=password)
        new_user = True
        print("New user created:", user)

        # Optionally create a token for the new user
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
                # Reduce drug quantity
                drug.quantity_available -= item['quantity']
                drug.save()
                print("Drug quantity updated for:", drug.name)

            # Generate PDF
            pdf_content = generate_order_pdf(order)
            pdf_attachment = {
                'filename': f'order_{order.id}.pdf',
                'content': pdf_content,
                'mime_type': 'application/pdf',
            }

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
            attachments = [pdf_attachment]

            if new_user:
                account_details_email = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Account Details</title>
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
                        <h1>Welcome, {user.username}!</h1>
                        <p>An account has been created for you with the following details:</p>
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>Password:</strong> {user.email}</p>
                        <p>Please feel free to log in and change your password and other details in your profile.</p>
                        <div class="footer">
                            <p>&copy; {datetime.now().year} Men's clinis. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                send_order_email(
                    subject='Your New Account Details',
                    html_content=account_details_email,
                    recipient_list=[user.email],
                    attachments=attachments
                )
                print("Account details email sent to:", user.email)

            send_order_email(
                subject='Order Confirmation',
                html_content=order_confirmation_email,
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


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        data = request.data
        images_data = data.pop('images', [])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        drug = serializer.save()
        
        for image_data in images_data:
            image_serializer = ImageSerializer(data={'image': image_data})
            image_serializer.is_valid(raise_exception=True)
            image = image_serializer.save()
            drug.images.add(image)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        images_data = data.pop('images', [])
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        drug = serializer.save()

        if images_data:
            drug.images.clear()
            for image_data in images_data:
                image_serializer = ImageSerializer(data={'image': image_data})
                image_serializer.is_valid(raise_exception=True)
                image = image_serializer.save()
                drug.images.add(image)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ConsultationCategoryViewSet(viewsets.ModelViewSet):
    queryset = ConsultationCategory.objects.all()
    serializer_class = ConsultationCategorySerializer
    permission_classes = [IsAuthenticated]


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


from datetime import datetime, timedelta
from django.db.models import Sum, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Existing imports...

@api_view(['GET'])
def sales_summary(request):
    try:
        today = datetime.today()
        start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        daily_sales = Order.objects.filter(created_at__gte=start_of_day).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
        monthly_sales = Order.objects.filter(created_at__gte=start_of_month).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
        yearly_sales = Order.objects.filter(created_at__gte=start_of_year).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0

        return Response({
            'daily_sales': daily_sales,
            'monthly_sales': monthly_sales,
            'yearly_sales': yearly_sales,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_statistics(request):
    try:
        most_purchases_user = Order.objects.values('user__username').annotate(total_spent=Sum('total_price')).order_by('-total_spent').first()
        if not most_purchases_user:
            most_purchases_user = {'user__username': 'None', 'total_spent': 0}

        return Response({
            'most_purchases_user': most_purchases_user['user__username'],
            'total_spent': most_purchases_user['total_spent'],
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def location_statistics(request):
    try:
        location_stats = Order.objects.values('country').annotate(total_sales=Sum('total_price')).order_by('-total_sales')

        return Response(location_stats, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
