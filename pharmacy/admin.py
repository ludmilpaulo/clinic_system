from django.contrib import admin

from pharmacy.forms import MultipleImageUploadForm
from .models import Drug, Image, Prescription, PrescriptionDrug, ConsultationCategory
from clinic_system.admin import custom_admin_site  # Import custom admin site

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity_available')
    search_fields = ('name',)
    list_filter = ('price',)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_number', 'patient', 'prescribed_by', 'issue_date')
    list_filter = ('issue_date', 'prescribed_by')
    search_fields = ('prescription_number', 'patient__user__username', 'prescribed_by__user__username')
    date_hierarchy = 'issue_date'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['drugs'].queryset = obj.drugs.all()
        return form

class PrescriptionDrugAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'drug', 'quantity')
    list_filter = ('drug',)
    search_fields = ('prescription__prescription_number', 'drug__name')

class ImageAdmin(admin.ModelAdmin):
    form = MultipleImageUploadForm

    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('image')
        for f in files:
            instance = Image(image=f)
            instance.save()

    def save_related(self, request, form, formsets, change):
        pass

    def response_add(self, request, obj, post_url_continue=None):
        return super().response_add(request, obj, post_url_continue)

custom_admin_site.register(ConsultationCategory)
custom_admin_site.register(Drug, DrugAdmin)
custom_admin_site.register(Image, ImageAdmin)
#custom_admin_site.register(PrescriptionDrug, PrescriptionDrugAdmin)

admin.site.register(ConsultationCategory)
admin.site.register(Drug, DrugAdmin)
admin.site.register(PrescriptionDrug, PrescriptionDrugAdmin)