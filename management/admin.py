# management/admin.py

from django import forms
from django.contrib import admin
from .models import DoctorAvailability

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'
        widgets = {
            'days_of_week': forms.CheckboxSelectMultiple(choices=DoctorAvailability.DAY_CHOICES)
        }

    def clean_days_of_week(self):
        data = self.cleaned_data['days_of_week']
        if isinstance(data, list):
            return ','.join(data)
        return data

class DoctorAvailabilityAdmin(admin.ModelAdmin):
    form = DoctorAvailabilityForm
    list_display = ('doctor', 'days_of_week', 'start_time', 'end_time', 'recurring_monthly')
    list_filter = ('recurring_monthly', 'doctor')
    search_fields = ('doctor__name', 'doctor__surname')

admin.site.register(DoctorAvailability, DoctorAvailabilityAdmin)
