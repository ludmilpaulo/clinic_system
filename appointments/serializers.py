from appointments.models import Appointment
from rest_framework import serializers
from management.models import DoctorAvailability



class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_surname = serializers.CharField(source='doctor.surname', read_only=True)
    category_name = serializers.CharField(source='consultation_category.name', read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'doctor_name', 'doctor_surname', 'consultation_category', 'category_name', 'days_of_week', 'start_time', 'end_time', 'recurring_monthly']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
