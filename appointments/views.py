from appointments.models import Appointment
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from management.models import DoctorAvailability
from .serializers import DoctorAvailabilitySerializer, AppointmentSerializer
class DoctorAvailabilityByCategory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        availabilities = DoctorAvailability.objects.filter(consultation_category=category_id)
        serializer = DoctorAvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)

class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(patient=self.request.user.patientprofile)
        except Exception as e:
            logger.error(f"Error creating appointment: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info(f"Request data: {request.data}")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Response data: {response.data}")
        return response