
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('appointment/', include('appointments.urls')),
    path('manager/', include('management.urls'))
]
