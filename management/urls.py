from django.urls import path
from .views import ConsultationCategoryList, DoctorAvailabilityListCreate

urlpatterns = [
    path('doctor-availability/', DoctorAvailabilityListCreate.as_view(), name='doctor-availability-list-create'),
    path('consultation-categories/', ConsultationCategoryList.as_view(), name='consultation-category-list'),
    # other URL patterns...
]
