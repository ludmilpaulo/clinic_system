from accounts.models import ConsultationCategory
from accounts.serializers import ConsultationCategorySerializer
import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import DoctorAvailability, DoctorProfile
from .serializers import DoctorAvailabilitySerializer

logger = logging.getLogger(__name__)

class DoctorAvailabilityListCreate(generics.ListCreateAPIView):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logger.info(f"Received data: {request.data}")
        try:
            user_id = request.data.get('user_id')
            if not user_id:
                raise ValidationError({'user_id': 'This field is required.'})
            
            try:
                doctor_profile = DoctorProfile.objects.get(user_id=user_id)
            except DoctorProfile.DoesNotExist:
                raise ValidationError({'doctor': f'Invalid pk "{user_id}" - object does not exist.'})
            
            request.data['doctor'] = doctor_profile.pk
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            logger.info(f"Validated data: {serializer.validated_data}")
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.error(f"Validation error: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
        
        
        
        
class DoctorAvailabilityList(generics.ListAPIView):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DoctorAvailability.objects.filter(doctor=user.doctorprofile)
    
    
class DoctorAvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DoctorAvailability.objects.filter(doctor=user.doctorprofile)



class ConsultationCategoryList(generics.ListAPIView):
    queryset = ConsultationCategory.objects.all()
    serializer_class = ConsultationCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

