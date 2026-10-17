"""
Generate synthetic test PDFs for development and testing.
Creates:
1. samples/sample_invoice.pdf (clean text-based invoice)
2. samples/sample_bol.pdf (clean text-based Bill of Lading)
3. samples/blank_sample.pdf (blank single page for OCR testing)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_sample_invoice(output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
    )
    story.append(Paragraph("TAX INVOICE", title_style))
    story.append(Spacer(1, 12))

    info_data = [
        [
            Paragraph("<b>Vendor / Supplier:</b><br/>Apex Industrial Supplies Ltd.<br/>742 Evergreen Terrace<br/>Springfield, OR 97477<br/>Tax ID: US-987654321", styles['Normal']),
            Paragraph("<b>Invoice Details:</b><br/>Invoice Number: <b>INV-2024-0042</b><br/>Invoice Date: <b>2024-10-15</b><br/>Due Date: <b>2024-11-14</b><br/>PO Number: <b>PO-99120</b><br/>Currency: <b>USD</b>", styles['Normal'])
        ],
        [
            Paragraph("<b>Customer / Bill To:</b><br/>Nexus Logistics Corp<br/>1200 Pacific Highway, Suite 400<br/>Seattle, WA 98101", styles['Normal']),
            Paragraph("<b>Payment Terms:</b><br/>Net 30 Days<br/>Bank Transfer: Acme Bank AC #98765432", styles['Normal'])
        ]
    ]
    info_table = Table(info_data, colWidths=[270, 270])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 16))

    items_data = [
        ["Description", "Qty", "Unit Price", "Total"],
        ["Heavy Duty Steel Strapping (5/8 in x 300 ft)", "10", "$45.00", "$450.00"],
        ["Industrial Pallet Shrink Wrap (18 in x 1500 ft)", "15", "$28.00", "$420.00"],
        ["Thermal Shipping Labels (Roll of 1000)", "8", "$18.50", "$148.00"],
        ["Subtotal", "", "", "$1,018.00"],
        ["Tax (8.5%)", "", "", "$86.53"],
        ["Freight / Shipping Charges", "", "", "$75.00"],
        ["Discount", "", "", "-$25.00"],
        ["Total Amount Due", "", "", "$1,154.53"],
    ]

    items_table = Table(items_data, colWidths=[310, 60, 85, 85])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, 3), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0, 4), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F1F5F9')),
        ('LINEABOVE', (0, 4), (-1, 4), 1, colors.HexColor('#0F172A')),
        ('LINEABOVE', (0, -1), (-1, -1), 1.5, colors.HexColor('#0F172A')),
    ]))
    story.append(items_table)
    doc.build(story)
    print(f"Created: {output_path}")

def create_sample_bol(output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'BolTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
    )
    story.append(Paragraph("OCEAN BILL OF LADING (MULTIMODAL)", title_style))
    story.append(Spacer(1, 10))

    parties_data = [
        [
            Paragraph("<b>Shipper / Exporter:</b><br/>Orient Global Manufacturing Ltd.<br/>88 Harbor Industrial Zone<br/>Shenzhen, Guangdong 518000, China", styles['Normal']),
            Paragraph("<b>Bill of Lading Number:</b> <b>BOL-ONEY-8829103</b><br/><b>Shipment Date:</b> 2024-09-28<br/><b>Carrier:</b> Ocean Network Express", styles['Normal'])
        ],
        [
            Paragraph("<b>Consignee:</b><br/>Pacific Imports & Distribution LLC<br/>2400 Maritime Way<br/>Long Beach, CA 90802, USA", styles['Normal']),
            Paragraph("<b>Notify Party:</b><br/>Pacific Imports Logistics Dept.<br/>Email: logistics@pacificimports.example<br/>Tel: +1-562-555-0199", styles['Normal'])
        ]
    ]
    parties_table = Table(parties_data, colWidths=[270, 270])
    parties_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
    ]))
    story.append(parties_table)
    story.append(Spacer(1, 10))

    voyage_data = [
        ["Place of Receipt", "Port of Loading", "Port of Discharge", "Final Destination"],
        ["Shenzhen CFS", "Port of Shenzhen, China", "Port of Long Beach, USA", "Long Beach, CA"],
        ["Vessel Name", "Voyage Number", "Container Number", "Seal Number"],
        ["EVER FORWARD", "V.042W", "ONEU9876543", "SL-554432"],
    ]
    voyage_table = Table(voyage_data, colWidths=[135, 135, 135, 135])
    voyage_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#F1F5F9')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,2), (-1,2), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(voyage_table)
    story.append(Spacer(1, 12))

    cargo_data = [
        ["Packages", "Description of Goods", "Gross Weight", "Measurement"],
        ["450 Cartons", "Precision Industrial Ball Bearings (Grade 5)\nHS Code: 8482.10\nClean On Board", "8,450.00 KGS", "28.5 CBM"]
    ]
    cargo_table = Table(cargo_data, colWidths=[90, 270, 100, 80])
    cargo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cargo_table)
    doc.build(story)
    print(f"Created: {output_path}")

def create_blank_pdf(output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    doc.build([Spacer(1, 100)])
    print(f"Created: {output_path}")

if __name__ == "__main__":
    os.makedirs("samples", exist_ok=True)
    create_sample_invoice("samples/sample_invoice.pdf")
    create_sample_bol("samples/sample_bol.pdf")
    create_blank_pdf("samples/blank_sample.pdf")
