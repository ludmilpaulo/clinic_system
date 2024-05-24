import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from accounts.models import DoctorProfile, PatientProfile


class Image(models.Model):
    image = models.ImageField(max_length=3000, default=None, blank=True, upload_to='drug_images/')

    def __str__(self):
        return self.image.name

class ConsultationCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Drug(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('ConsultationCategory', related_name='drugs', on_delete=models.CASCADE, null=True)
    images = models.ManyToManyField('Image')
    description = CKEditor5Field('Text', config_name='extends')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.quantity_available} in stock"

    @property
    def category_name(self):
        return self.category.name if self.category else ''

    @property
    def image_urls(self):
        return [image.image.url for image in self.images.all()]





class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    prescribed_by = models.ForeignKey(DoctorProfile, related_name="prescriber", on_delete=models.CASCADE)
    drugs = models.ManyToManyField(Drug, through='PrescriptionDrug')
    issue_date = models.DateField(auto_now_add=True)
    prescription_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription {self.prescription_number} for {self.patient.user.username}"

class PrescriptionDrug(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.drug.name}"


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    drugs = models.ManyToManyField(Drug, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    drugs = models.ManyToManyField(Drug, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Revenue(models.Model):
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
