from rest_framework import serializers
from .models import DoctorAvailability

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    days_of_week = serializers.ListField(
        child=serializers.ChoiceField(choices=DoctorAvailability.DAY_CHOICES),
        allow_empty=True
    )

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'consultation_category', 'days_of_week', 'day_of_month', 'start_time', 'end_time', 'year', 'month', 'recurring_monthly']

    def validate_days_of_week(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Expected a list of items but got type 'str'.")
        day_choices = [choice[0] for choice in DoctorAvailability.DAY_CHOICES]
        for day in value:
            if day not in day_choices:
                raise serializers.ValidationError(f"{day} is not a valid choice")
        return value

    def create(self, validated_data):
        validated_data['days_of_week'] = ','.join(validated_data['days_of_week']) if validated_data['days_of_week'] else ''
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['days_of_week'] = ','.join(validated_data['days_of_week']) if validated_data['days_of_week'] else ''
        return super().update(instance, validated_data)
