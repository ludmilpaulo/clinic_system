import os
from datetime import datetime
from django.contrib.auth.models import User
from accounts.models import ConsultationCategory
from accounts.serializers import ConsultationCategorySerializer
from clinic_system.settings import MEDIA_ROOT
from pharmacy.models import Drug, Image
from datetime import datetime
from rest_framework.decorators import action
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



from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now


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
        # Check if user with the email already exists
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
            print("Existing user retrieved:", user)
        except User.DoesNotExist:
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

            # Ensure media directory exists
            os.makedirs(os.path.join(MEDIA_ROOT, 'invoices'), exist_ok=True)

            # Generate PDF
            pdf_content = generate_order_pdf(order)
            pdf_path = f'{MEDIA_ROOT}/invoices/order_{order.id}.pdf'
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_content)
            order.invoice = f'invoices/order_{order.id}.pdf'
            order.save(update_fields=['invoice'])

            # Render the order confirmation email template
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

def send_order_email(subject, message, recipient_list, attachments=None):
    email = EmailMessage(
        subject,
        message,
        'no-reply@example.com',
        recipient_list,
    )
    if attachments:
        for attachment in attachments:
            email.attach(attachment['filename'], attachment['content'], attachment['mime_type'])
    email.content_subtype = 'html'  # This is necessary to send HTML email
    email.send()


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
    permission_classes = [AllowAny]
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get('status')
        if status not in dict(Order.STATUS_CHOICES):
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status
        order.save()
        return Response(OrderSerializer(order).data)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]


from datetime import datetime, timedelta
from django.db.models import Sum, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Existing imports...
from .models import Order  # Ensure the correct import path for your Order model

@api_view(['GET'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def location_statistics(request):
    try:
        location_stats = Order.objects.values('country').annotate(total_sales=Sum('total_price')).order_by('-total_sales')

        return Response(location_stats, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
