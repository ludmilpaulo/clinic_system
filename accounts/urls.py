from django.urls import path, include
from accounts.views import DoctorProfileDetail, custom_login, custom_signup




urlpatterns = [
    path('custom-login/', custom_login, name='custom-login'),
    path('custom-signup/', custom_signup, name='custom-signup'),
    path('doctor-profile/<int:doctor_id>/', DoctorProfileDetail.as_view(), name='doctor-profile-detail'),
]
