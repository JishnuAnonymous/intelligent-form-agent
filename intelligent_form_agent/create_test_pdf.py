from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "OFFICIAL INVOICE")
    
    # Content
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Date: 2026-03-15")
    c.drawString(50, height - 120, "Invoice #: INV-2026-999")
    c.drawString(50, height - 140, "Customer Name: Johnathan Doe")
    c.drawString(50, height - 160, "Email: john.doe@example.com")
    c.drawString(50, height - 180, "Phone: 555-0199")
    
    c.drawString(50, height - 220, "Description of Services:")
    c.drawString(70, height - 240, "- Software Development Consulting: $1000.00")
    c.drawString(70, height - 260, "- Server Maintenance: $250.00")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 300, "Total Amount: $1250.00")
    
    # Signature Line
    c.line(50, height - 400, 250, height - 400)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, height - 415, "Authorized Signature: Johnathan Doe")
    
    c.save()
    print(f"Created PDF: {filename}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    create_pdf("data/test_form.pdf")
