from rest_framework import serializers
from .models import DoctorAvailability

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    days_of_week = serializers.ListField(child=serializers.ChoiceField(choices=DoctorAvailability.DAY_CHOICES))

    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'consultation_category', 'days_of_week', 'start_time', 'end_time', 'recurring_monthly']

    def validate_days_of_week(self, value):
        day_choices = [choice[0] for choice in DoctorAvailability.DAY_CHOICES]
        for day in value:
            if day not in day_choices:
                raise serializers.ValidationError(f"{day} is not a valid choice")
        return value

    def create(self, validated_data):
        days_of_week = ','.join(validated_data.pop('days_of_week'))
        validated_data['days_of_week'] = days_of_week
        return super().create(validated_data)

    def update(self, instance, validated_data):
        days_of_week = ','.join(validated_data.pop('days_of_week'))
        validated_data['days_of_week'] = days_of_week
        return super().update(instance, validated_data)
