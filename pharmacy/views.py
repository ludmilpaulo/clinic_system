from accounts.models import ConsultationCategory
from accounts.serializers import ConsultationCategorySerializer
from appointments.models import Appointment, MedicalRecord
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import *
from rest_framework.decorators import *
from rest_framework.permissions import *
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Cart, Order, Prescription,  Drug, Revenue
from .serializers import AppointmentSerializer, CartSerializer, OrderSerializer, PrescriptionSerializer, MedicalRecordSerializer, DrugSerializer, RevenueSerializer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

class AppointmentListView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Appointment.objects.filter(doctor__user=user_id)
        appointment_time = self.request.query_params.get('appointment_time', None)
        if appointment_time:
            parsed_time = parse_datetime(appointment_time)
            if parsed_time:
                queryset = queryset.filter(appointment_time=parsed_time)
        return queryset

class PrescriptionListView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prescription.objects.filter(prescribed_by__user=self.kwargs['user_id'])

class MedicalRecordListView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient__user=self.kwargs['user_id'])

class DrugListView(generics.ListAPIView):
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Drug.objects.all()


class PrescriptionCreateView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


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



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class RevenueViewSet(viewsets.ModelViewSet):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def drug_list(request):
    if request.method == 'GET':
        drugs = Drug.objects.all()
        serializer = DrugSerializer(drugs, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DrugSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def drug_detail(request, pk):
    try:
        drug = Drug.objects.get(pk=pk)
    except Drug.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrugSerializer(drug, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DrugSerializer(drug, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drug.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    categories = ConsultationCategory.objects.all()
    serializer = ConsultationCategorySerializer(categories, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def search_drugs(request):
    query = request.GET.get('query', '')
    if query:
        drugs = Drug.objects.filter(name__icontains=query)
        serializer = DrugSerializer(drugs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No query parameter provided."}, status=status.HTTP_400_BAD_REQUEST)
