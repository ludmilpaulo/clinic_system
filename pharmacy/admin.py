from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path

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
    change_list_template = "admin/multiple_upload.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('multiple_upload/', self.admin_site.admin_view(self.multiple_upload), name='multiple_image_upload'),
        ]
        return custom_urls + urls

    def multiple_upload(self, request):
        if request.method == 'POST':
            form = MultipleImageUploadForm(request.POST, request.FILES)
            files = request.FILES.getlist('images')
            if form.is_valid():
                for f in files:
                    instance = Image(image=f)
                    instance.save()
                self.message_user(request, "Images uploaded successfully")
                return redirect("admin:pharmacy_image_changelist")
        else:
            form = MultipleImageUploadForm()
        context = {
            'form': form,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
        }
        return render(request, "admin/multiple_upload.html", context)

custom_admin_site.register(ConsultationCategory)
custom_admin_site.register(Drug, DrugAdmin)
custom_admin_site.register(Image, ImageAdmin)
#custom_admin_site.register(PrescriptionDrug, PrescriptionDrugAdmin)

admin.site.register(ConsultationCategory)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Image, ImageAdmin) 
admin.site.register(PrescriptionDrug, PrescriptionDrugAdmin)