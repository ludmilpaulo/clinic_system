from rest_framework import serializers
from .models import AboutUs, Contact, Why_Choose_Us, Testimonial

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'

class WhyChooseUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Why_Choose_Us
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'