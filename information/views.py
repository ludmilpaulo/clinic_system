from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import AboutUs, Why_Choose_Us, Testimonial
from .serializers import AboutUsSerializer, ContactSerializer, WhyChooseUsSerializer, TestimonialSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def about_us(request):
    about = AboutUs.objects.first()
    why_choose_us = Why_Choose_Us.objects.all()
    testimonials = Testimonial.objects.all()

    about_serializer = AboutUsSerializer(about, context={'request': request})
    why_choose_us_serializer = WhyChooseUsSerializer(why_choose_us, many=True)
    testimonial_serializer = TestimonialSerializer(testimonials, many=True)

    return Response({
        'about': about_serializer.data,
        'why_choose_us': why_choose_us_serializer.data,
        'testimonials': testimonial_serializer.data,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
