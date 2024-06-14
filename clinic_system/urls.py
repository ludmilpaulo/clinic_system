from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin import custom_admin_site  # Import the custom admin site

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # Use custom admin site here
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
