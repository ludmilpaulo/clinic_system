# views.py

from rest_framework import viewsets
from .models import Appointment, DoctorProfile, ConsultationCategory
from .serializers import AppointmentSerializer, DoctorProfileSerializer, ConsultationCategorySerializer
from django.utils.timezone import make_aware
from datetime import datetime

class ConsultationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConsultationCategory.objects.all()
    serializer_class = ConsultationCategorySerializer

class DoctorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return DoctorProfile.objects.filter(category_id=category_id)
        return DoctorProfile.objects.all()

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor')
        date_time = self.request.query_params.get('datetime')

        if doctor_id and date_time:
            aware_date_time = make_aware(datetime.fromisoformat(date_time))
            queryset = queryset.filter(doctor_id=doctor_id, appointment_time=aware_date_time)

        return queryset
