from django.urls import path
from .views import DoctorAppointmentsView, DoctorAvailabilityByCategory, AppointmentCreateView

urlpatterns = [
    path('doctor-availability/<int:category_id>/', DoctorAvailabilityByCategory.as_view(), name='doctor-availability-by-category'),
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('doctor-appointments/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    path('doctor-appointments/<int:doctor_id>/', DoctorAppointmentsView.as_view(), name='doctor-appointments-detail'),
]
