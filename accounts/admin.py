from django.contrib import admin
from .models import ConsultationCategory, PatientProfile, DoctorProfile, ManagementProfile

@admin.register(ConsultationCategory)
class ConsultationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'phone_number', 'id_number_or_passport')
    search_fields = ('name', 'surname', 'id_number_or_passport')

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'specialty', 'years_of_experience')
    search_fields = ('name', 'surname', 'specialty')

@admin.register(ManagementProfile)
class ManagementProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'position')
    search_fields = ('name', 'surname', 'position')