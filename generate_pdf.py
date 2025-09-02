from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

def generate_pdf(path, donation_id, name, email, amount, donation_type, address):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # ✅ Watermark
    watermark = ImageReader('static/watermark.jpg')
    wm_width = width * 0.65
    wm_height = height * 0.65
    wm_x = (width - wm_width) / 2
    wm_y = (height - wm_height) / 2

    c.saveState()
    c.setFillAlpha(0.1)
    c.drawImage(watermark, wm_x, wm_y, width=wm_width, height=wm_height, mask='auto')
    c.restoreState()

    # ✅ Header
    header = ImageReader('static/header.jpg')
    header_height = 100
    c.drawImage(header, 0, height - header_height, width=width, height=header_height)

    # ✅ Title
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - header_height - 40, "Donation Receipt")

    # ✅ Donation details (smaller size)
    y = height - header_height - 90
    label_font = 16
    value_font = 16
    line_height = 30

    details = [
        ("Donation ID:", donation_id),
        ("Name:", name),
        ("Email:", email),
        ("Address:", address),
        ("Donation Type:", donation_type),
        ("Amount:", f"{amount} (Rupees)"),
        ("Date:", datetime.now().strftime('%d-%m-%Y'))
    ]

    for label, value in details:
        c.setFont("Helvetica-Bold", label_font)
        c.drawString(50, y, label)
        c.setFont("Helvetica", value_font)
        c.drawString(200, y, str(value))
        y -= line_height

    # ✅ Signature (larger than before)
    y -= 20
    sig = ImageReader('static/signature.png')
    sig_width = 300  # increased
    sig_height = 120  # increased
    c.drawImage(sig, (width - sig_width) / 2, y - sig_height, width=sig_width, height=sig_height)

    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, y - sig_height - 15, "Authorized Signature")

    # ✅ Footer
    footer = ImageReader('static/footer.jpg')
    footer_height = 100
    c.drawImage(footer, 0, 0, width=width, height=footer_height)

    # ✅ Save PDF
    c.save()
