from accounts.models import ConsultationCategory
from accounts.serializers import ConsultationCategorySerializer
from rest_framework import generics, permissions
from .models import DoctorAvailability
from .serializers import DoctorAvailabilitySerializer

class DoctorAvailabilityListCreate(generics.ListCreateAPIView):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctorprofile)





class ConsultationCategoryList(generics.ListAPIView):
    queryset = ConsultationCategory.objects.all()
    serializer_class = ConsultationCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

