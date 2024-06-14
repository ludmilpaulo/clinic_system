from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class CustomAdminSite(admin.AdminSite):
    site_header = _("Men's Clinic - Comprehensive Men's Health Solutions")
    site_title = _("Men's Clinic Admin")
    index_title = _("Welcome to Men's Clinic Administration")

custom_admin_site = CustomAdminSite()

# Register your models here using custom_admin_site instead of admin.site
# Example:
# from .models import YourModel
# custom_admin_site.register(YourModel)
