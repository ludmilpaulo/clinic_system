from appointments.models import Appointment
from management.models import DoctorAvailability
from rest_framework import serializers



class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor_user_id = serializers.IntegerField(source='doctor.user.id', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_surname = serializers.CharField(source='doctor.surname', read_only=True)
    category_name = serializers.CharField(source='consultation_category.name', read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor_user_id', 'doctor_name', 'doctor_surname', 'consultation_category', 'category_name', 'days_of_week', 'day_of_month', 'start_time', 'end_time', 'year', 'month', 'recurring_monthly', 'booked']




class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'
    
    def get_patient_name(self, obj):
        return f"{obj.patient.name} {obj.patient.surname}"
