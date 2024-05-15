# management/models.py

from django.db import models
from accounts.models import ConsultationCategory, DoctorProfile

class DaysOfWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13  # Maximum length for the comma-separated days
        super().__init__(*args, **kwargs)

class DoctorAvailability(models.Model):
    DAY_CHOICES = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    consultation_category = models.ForeignKey(ConsultationCategory, on_delete=models.CASCADE)
    days_of_week = DaysOfWeekField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurring_monthly = models.BooleanField(default=False, help_text="Check if this availability recurs every month")

    def __str__(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days = [day_names[int(day)] for day in self.days_of_week.split(',')]
        days_str = ', '.join(days)
        return f"{self.doctor.name} available on {days_str} from {self.start_time} to {self.end_time}"

    class Meta:
        unique_together = ('doctor', 'days_of_week', 'start_time', 'end_time', 'recurring_monthly')
