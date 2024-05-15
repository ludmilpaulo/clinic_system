from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, DoctorProfileViewSet, ConsultationCategoryViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'doctors', DoctorProfileViewSet)
router.register(r'categories', ConsultationCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
