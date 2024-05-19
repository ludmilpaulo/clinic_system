from django.urls import path
from .views import about_us, submit_contact

urlpatterns = [
    path('about-us/', about_us, name='about-us'),
    path('submit-contact/', submit_contact, name='submit-contact'),
]
