from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from information.models import AboutUs
from weasyprint import HTML
import os
from .models import Order


from io import BytesIO

from xhtml2pdf import pisa

def generate_order_pdf(order, request):
    about_us = AboutUs.objects.first()  # Assuming there's only one AboutUs entry
    html_string = render_to_string('invoice_template.html', {'order': order, 'about_us': about_us})
    
    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=buffer, link_callback=lambda uri, rel: request.build_absolute_uri(uri))

    if pisa_status.err:
        return None

    buffer.seek(0)
    return buffer.read()

def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    pdf = generate_order_pdf(order)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'
    return response
