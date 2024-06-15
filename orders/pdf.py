from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from information.models import AboutUs
from weasyprint import HTML
import os
from .models import Order

def generate_order_pdf(order, request):
    about_us = AboutUs.objects.first()  # Assuming there's only one AboutUs entry
    html_string = render_to_string('invoice_template.html', {'order': order, 'about_us': about_us})
    
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()

    return pdf_file

def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    pdf = generate_order_pdf(order)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'
    return response
