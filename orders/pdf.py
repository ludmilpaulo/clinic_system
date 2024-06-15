from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_order_pdf(order):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Order {order.id}")

    pdf.drawString(100, 750, f"Order ID: {order.id}")
    pdf.drawString(100, 730, f"User: {order.user.username}")
    pdf.drawString(100, 710, f"Total Price: {order.total_price}")
    pdf.drawString(100, 690, f"Address: {order.address}, {order.city}, {order.postal_code}, {order.country}")
    pdf.drawString(100, 670, f"Payment Method: {order.payment_method}")
    pdf.drawString(100, 650, "Items:")

    y = 630
    for item in order.items.all():
        pdf.drawString(100, y, f"{item.quantity} x {item.drug.name} @ {item.price} each")
        y -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer.read()
