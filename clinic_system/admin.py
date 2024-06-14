from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

admin.site.site_header = "Men's Clinic - Comprehensive Men's Health Solutions"
admin.site.site_title = "Men's Clinic Admin"
admin.site.index_title = "Welcome to Men's Clinic Administration"

class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['site_header'] = self.site_header
        context['site_title'] = self.site_title
        context['index_title'] = self.index_title
        context['custom_admin_css'] = 'css/custom_admin.css'
        return context

custom_admin_site = CustomAdminSite()

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('account/', include('accounts.urls')),
    path('appointment/', include('appointments.urls')),
    path('manager/', include('management.urls')),
    path('info/', include('information.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('order/', include('orders.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
