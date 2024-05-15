from rest_framework import serializers
from .models import DoctorAvailability

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'consultation_category', 'days_of_week', 'start_time', 'end_time', 'recurring_monthly']
