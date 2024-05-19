import logging
from appointments.models import Appointment, MedicalRecord
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework import generics, serializers, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

from management.models import DoctorAvailability
from accounts.models import DoctorProfile, PatientProfile, User
from .serializers import DoctorAvailabilitySerializer, AppointmentSerializer

logger = logging.getLogger(__name__)
class DoctorAvailabilityByCategory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        availabilities = DoctorAvailability.objects.filter(consultation_category_id=category_id)
        serializer = DoctorAvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)



class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient')
        doctor_id = request.data.get('doctor')
        appointment_time = request.data.get('appointment_time')

        print(f"Received data: patient_id={patient_id}, doctor_id={doctor_id}")

        try:
            # Fetch and validate the patient
            patient_user = User.objects.get(pk=patient_id)
            print(f"Fetched patient_user: {patient_user}")
            patient_profile = PatientProfile.objects.get(user=patient_user)
            print(f"Fetched patient_profile: {patient_profile}")
            request.data['patient'] = patient_profile.pk

            # Fetch and validate the doctor
            doctor_user = User.objects.get(pk=doctor_id)
            print(f"Fetched doctor_user: {doctor_user}")
            doctor_profile = DoctorProfile.objects.get(user=doctor_user)
            print(f"Fetched doctor_profile: {doctor_profile}")
            request.data['doctor'] = doctor_profile.pk

            # Check for existing appointment
            existing_appointment = Appointment.objects.filter(
                doctor=doctor_profile,
                appointment_time=appointment_time
            ).first()
            
            if existing_appointment:
                raise ValidationError("An appointment with this doctor at this time already exists.")

            # Save the appointment with the patient and doctor profiles
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except User.DoesNotExist:
            print("User does not exist.")
            raise ValidationError("User does not exist.")
        except PatientProfile.DoesNotExist:
            print("Patient profile does not exist for the user.")
            raise ValidationError("Patient profile does not exist for the user.")
        except DoctorProfile.DoesNotExist:
            print("Doctor profile does not exist for the user.")
            raise ValidationError("Doctor profile does not exist for the user.")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise ValidationError(f"Unexpected error: {str(e)}")



class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(doctor=user.doctorprofile)





def generate_pdf(data, title):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, f"Title: {title}")
    c.drawString(100, height - 120, f"Patient: {data['patient_name']}")
    c.drawString(100, height - 140, f"Date: {data['date']}")
    c.drawString(100, height - 160, f"Details: {data['details']}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def download_medical_record(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    data = {
        'patient_name': f"{medical_record.patient.user.first_name} {medical_record.patient.user.last_name}",
        'date': medical_record.record_date,
        'details': f"Diagnosis: {medical_record.diagnosis}\nTreatment: {medical_record.treatment}",
    }
    buffer = generate_pdf(data, "Medical Record")
    return FileResponse(buffer, as_attachment=True, filename='medical_record.pdf')

def download_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    drugs = "\n".join([f"{pd.quantity} of {pd.drug.name}" for pd in prescription.prescriptiondrug_set.all()])
    data = {
        'patient_name': f"{prescription.patient.user.first_name} {prescription.patient.user.last_name}",
        'date': prescription.issue_date,
        'details': f"Drugs:\n{drugs}\nNotes: {prescription.notes}",
    }
    buffer = generate_pdf(data, "Prescription")
    return FileResponse(buffer, as_attachment=True, filename='prescription.pdf')