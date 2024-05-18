from django.contrib import admin
from .models import DoctorAvailability
from .forms import DoctorAvailabilityForm

class DoctorAvailabilityAdmin(admin.ModelAdmin):
    form = DoctorAvailabilityForm
    list_display = ('doctor', 'get_days_of_week', 'start_time', 'end_time', 'recurring_monthly')
    list_filter = ('recurring_monthly', 'doctor')
    search_fields = ('doctor__name', 'doctor__surname')

    def get_days_of_week(self, obj):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days = [day_names[int(day)] for day in obj.days_of_week.split(',')]
        return ', '.join(days)
    get_days_of_week.short_description = 'Days of Week'

    def save_model(self, request, obj, form, change):
        obj.days_of_week = ','.join(form.cleaned_data.get('days_of_week'))
        super().save_model(request, obj, form, change)

admin.site.register(DoctorAvailability, DoctorAvailabilityAdmin)
