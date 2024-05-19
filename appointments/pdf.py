from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

def generate_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, f"Patient: {data['patient_name']}")
    c.drawString(100, height - 120, f"Date: {data['record_date']}")
    c.drawString(100, height - 140, f"Diagnosis: {data['diagnosis']}")
    c.drawString(100, height - 160, f"Treatment: {data['treatment']}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
