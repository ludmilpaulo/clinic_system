from django.contrib import admin
from .models import Appointment, MedicalRecord, Billing

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'category', 'appointment_time', 'status', 'paid', 'fee')
    search_fields = ('patient__name', 'doctor__name', 'appointment_time', 'status')
    list_filter = ('status', 'paid')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_date', 'doctor')
    search_fields = ('patient__name', 'record_date', 'doctor__name')

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service_name', 'service_fee', 'billing_date', 'paid')
    search_fields = ('patient__name', 'service_name', 'billing_date')
    list_filter = ('paid',)
