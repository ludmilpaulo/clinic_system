# serializers.py

from rest_framework import serializers
from .models import Appointment, DoctorProfile, ConsultationCategory

class ConsultationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationCategory
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    category = ConsultationCategorySerializer()

    class Meta:
        model = DoctorProfile
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    patient = serializers.StringRelatedField()

    class Meta:
        model = Appointment
        fields = '__all__'
