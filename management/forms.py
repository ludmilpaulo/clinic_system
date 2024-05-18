from django import forms
from .models import DoctorAvailability

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'
        widgets = {
            'days_of_week': forms.CheckboxSelectMultiple(choices=DoctorAvailability.DAY_CHOICES),
        }

    def clean_days_of_week(self):
        data = self.cleaned_data['days_of_week']
        if isinstance(data, list):
            return ','.join(data)
        return data
