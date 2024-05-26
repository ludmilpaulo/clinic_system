# views.py

from datetime import datetime
from accounts.models import ConsultationCategory
from accounts.serializers import ConsultationCategorySerializer
from pharmacy.models import Drug, Image
from pharmacy.serializers import DrugSerializer, ImageSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import  Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
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
