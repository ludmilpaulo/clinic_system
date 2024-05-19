from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Drug, Image, Order, OrderItem, BaseProfile
from .serializers import DrugSerializer, ImageSerializer, OrderSerializer, BaseProfileSerializer

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        drug = self.get_object()
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            drug.images.add(serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class BaseProfileViewSet(viewsets.ModelViewSet):
    queryset = BaseProfile.objects.all()
    serializer_class = BaseProfileSerializer

    @action(detail=False, methods=['get'])
    def revenue(self, request):
        # Calculate revenue and return data
        # Example response structure
        data = {
            "weekly_sales": [100, 200, 150, 300, 250, 400, 500],
            "monthly_sales": [1000, 2000, 1500, 3000, 2500, 4000, 5000],
            "most_bought_product": "Paracetamol",
            "total_revenue": 15000
        }
        return Response(data)
