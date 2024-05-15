from django.contrib.auth.models import User
from django.db import models

from accounts.models import DoctorProfile, PatientProfile

class Drug(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.quantity_available} in stock"

class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    prescribed_by = models.ForeignKey(DoctorProfile, related_name="prescriber", on_delete=models.CASCADE)
    drugs = models.ManyToManyField(Drug, through='PrescriptionDrug')
    issue_date = models.DateField(auto_now_add=True)
    prescription_number = models.CharField(max_length=20, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription {self.prescription_number} for {self.patient.user.username}"

class PrescriptionDrug(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.drug.name}"

