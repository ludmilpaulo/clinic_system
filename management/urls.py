from django.urls import path
from .views import ConsultationCategoryList, DoctorAvailabilityDetail, DoctorAvailabilityList, DoctorAvailabilityListCreate

urlpatterns = [
    path('doctor-availability/', DoctorAvailabilityListCreate.as_view(), name='doctor-availability-list-create'),
    path('doctor-availabilities/', DoctorAvailabilityList.as_view(), name='doctor-availability-list'),
    path('doctor-availability/<int:pk>/', DoctorAvailabilityDetail.as_view(), name='doctor-availability-detail'),
    path('consultation-categories/', ConsultationCategoryList.as_view(), name='consultation-category-list'),
    # other URL patterns...
]
