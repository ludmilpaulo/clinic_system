from django.urls import path
from .views import (
    AppointmentListView,
    PrescriptionCreateView,
    PrescriptionListView,
    MedicalRecordListView,
    DrugListView,
    category_list,
    download_medical_record,
    download_prescription,
    drug_detail,
    drug_list,
    search_drugs
)

urlpatterns = [
    path('appointments/<int:user_id>/', AppointmentListView.as_view(), name='appointment-list'),
    path('prescriptions/<int:user_id>/', PrescriptionListView.as_view(), name='prescription-list'),
    path('medical-records/<int:user_id>/', MedicalRecordListView.as_view(), name='medical-record-list'),
    path('pharmacy/prescriptions/', PrescriptionCreateView.as_view(), name='prescription-create'),
    path('drugs/', DrugListView.as_view(), name='drug-list'),
    path('download-medical-record/<int:pk>/', download_medical_record, name='download-medical-record'),
    path('download-prescription/<int:pk>/', download_prescription, name='download-prescription'),
    #############################################################################################
    path('pharmacy/drugs/', drug_list, name='drug-list'),
    path('search/', search_drugs, name='search_drugs'),
    path('pharmacy/detail/<int:pk>/', drug_detail, name='drug-detail'),
    path('pharmacy/categories/', category_list, name='category-list'),
]
