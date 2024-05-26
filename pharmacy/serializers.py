from appointments.models import Appointment, MedicalRecord
from orders.models import Order
from rest_framework import serializers
from .models import  Image, Prescription, PrescriptionDrug, Drug, Cart, Revenue

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient_name(self, obj):
        return f"{obj.patient.name} {obj.patient.surname}"

    def get_doctor_name(self, obj):
        return f"{obj.doctor.name} {obj.doctor.surname}"

    def get_category_name(self, obj):
        return obj.category.name

class PrescriptionDrugSerializer(serializers.ModelSerializer):
    drug_name = serializers.SerializerMethodField()

    class Meta:
        model = PrescriptionDrug
        fields = '__all__'

    def get_drug_name(self, obj):
        return obj.drug.name

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    prescribed_by_name = serializers.SerializerMethodField()
    drugs = PrescriptionDrugSerializer(many=True, source='prescriptiondrug_set')

    class Meta:
        model = Prescription
        fields = '__all__'

    def get_patient_name(self, obj):
        return f"{obj.patient.name} {obj.patient.name}"

    def get_prescribed_by_name(self, obj):
        return f"{obj.prescribed_by.user.first_name} {obj.prescribed_by.user.last_name}"
    
    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs')
        prescription = Prescription.objects.create(**validated_data)
        for drug_data in drugs_data:
            PrescriptionDrug.objects.create(prescription=prescription, **drug_data)
        return prescription

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = '__all__'

    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"

    def get_doctor_name(self, obj):
        return obj.doctor.user.username if obj.doctor else 'Unknown'





class DrugSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Drug
        fields = ['id', 'name', 'description', 'price', 'quantity_available', 'image_urls', 'category_name']

    def get_image_urls(self, obj):
        if obj.images.exists():
            request = self.context.get('request')
            if request is not None:
                return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        return []



######################################################################################
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = '__all__'