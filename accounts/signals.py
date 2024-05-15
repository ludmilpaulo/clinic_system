# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PatientProfile, DoctorProfile, ManagementProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check the group assignment to determine the profile type
        if instance.groups.filter(name="Patients").exists():
            PatientProfile.objects.create(user=instance)
        elif instance.groups.filter(name="Doctors").exists():
            DoctorProfile.objects.create(user=instance)
        elif instance.groups.filter(name="Management").exists():
            ManagementProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "patientprofile"):
        instance.patientprofile.save()
    elif hasattr(instance, "doctorprofile"):
        instance.doctorprofile.save()
    elif hasattr(instance, "managementprofile"):
        instance.managementprofile.save()
