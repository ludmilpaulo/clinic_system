from django.contrib import admin
from .models import Drug, Prescription, PrescriptionDrug

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity_available')
    search_fields = ('name',)
    list_filter = ('price',)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_number', 'patient', 'prescribed_by', 'issue_date')
    list_filter = ('issue_date', 'prescribed_by')
    search_fields = ('prescription_number', 'patient__user__username', 'prescribed_by__user__username')
    date_hierarchy = 'issue_date'

    # This method is used to display drugs in the prescription within the admin change view
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['drugs'].queryset = obj.drugs.all()
        return form

class PrescriptionDrugAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'drug', 'quantity')
    list_filter = ('drug',)
    search_fields = ('prescription__prescription_number', 'drug__name')

# Register your models here.
admin.site.register(Drug, DrugAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(PrescriptionDrug, PrescriptionDrugAdmin)
