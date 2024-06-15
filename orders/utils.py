import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_order_pdf(order):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Order Confirmation for Order #{order.id}")
    p.drawString(100, 730, f"Total Price: {order.total_price} Kz")
    p.drawString(100, 710, f"Address: {order.address}, {order.city}, {order.postal_code}, {order.country}")
    p.drawString(100, 690, f"Payment Method: {order.payment_method}")

    p.drawString(100, 650, "Order Items:")
    height = 630
    for item in order.items.all():
        p.drawString(100, height, f"{item.quantity} x {item.drug.name} at {item.price} Kz each")
        height -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer.getvalue()
