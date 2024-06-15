from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin import custom_admin_site  # Import custom admin site

urlpatterns = [
    path('clinic/admin/', custom_admin_site.urls, name='custom_admin'),  # Use custom admin site here with unique namespace
   # path('original-admin/', admin.site.urls, name='admin'),  # Use original admin site here with unique namespace
    path('account/', include('accounts.urls')),
    path('appointment/', include('appointments.urls')),
    path('manager/', include('management.urls')),
    path('info/', include('information.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('order/', include('orders.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
