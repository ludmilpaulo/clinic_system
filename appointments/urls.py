from django.urls import path
from .views import DoctorAvailabilityByCategory, AppointmentCreateView

urlpatterns = [
    path('doctor-availability/<int:category_id>/', DoctorAvailabilityByCategory.as_view(), name='doctor-availability-by-category'),
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
]
