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

def create_consulting_invoice(output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
    )
    story.append(Paragraph("CONSULTING SERVICES INVOICE", title_style))
    story.append(Spacer(1, 12))

    info_data = [
        [
            Paragraph("<b>Vendor / Service Provider:</b><br/>CloudScale Architecture LLC<br/>500 Cloud Parkway, Suite 300<br/>Austin, TX 78701<br/>Email: billing@cloudscalellc.example", styles['Normal']),
            Paragraph("<b>Invoice Details:</b><br/>Invoice Number: <b>INV-2024-789</b><br/>Invoice Date: <b>2024-11-01</b><br/>Due Date: <b>2024-11-16</b><br/>PO Number: <b>PO-88310</b><br/>Currency: <b>USD</b>", styles['Normal'])
        ],
        [
            Paragraph("<b>Client / Bill To:</b><br/>FinTech Ventures Inc<br/>100 Wall Street, 18th Floor<br/>New York, NY 10005", styles['Normal']),
            Paragraph("<b>Payment Terms:</b><br/>Net 15 Days<br/>Direct Deposit / ACH Wire Transfer", styles['Normal'])
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
        ["Description", "Hours", "Rate", "Total"],
        ["Cloud Architecture & Security Audit (80 Hours @ $175.00)", "80", "$175.00", "$14,000.00"],
        ["Subtotal", "", "", "$14,000.00"],
        ["Tax (0%)", "", "", "$0.00"],
        ["Shipping / Handling", "", "", "$0.00"],
        ["Discount", "", "", "$0.00"],
        ["Total Amount Due", "", "", "$14,000.00"],
    ]

    items_table = Table(items_data, colWidths=[310, 60, 85, 85])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, 1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0, 2), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F1F5F9')),
        ('LINEABOVE', (0, 2), (-1, 2), 1, colors.HexColor('#0F172A')),
        ('LINEABOVE', (0, -1), (-1, -1), 1.5, colors.HexColor('#0F172A')),
    ]))
    story.append(items_table)
    doc.build(story)
    print(f"Created: {output_path}")

def create_international_invoice(output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
    )
    story.append(Paragraph("COMMERCIAL INVOICE", title_style))
    story.append(Spacer(1, 12))

    info_data = [
        [
            Paragraph("<b>Vendor / Supplier:</b><br/>Berlin Sensorik GmbH<br/>Alexanderplatz 12<br/>10178 Berlin, Germany<br/>VAT ID: DE-123456789", styles['Normal']),
            Paragraph("<b>Invoice Details:</b><br/>Invoice Number: <b>INV-EU-9921</b><br/>Invoice Date: <b>2024-10-20</b><br/>Due Date: <b>2024-11-20</b><br/>PO Number: <b>PO-NOR-4410</b><br/>Currency: <b>EUR</b>", styles['Normal'])
        ],
        [
            Paragraph("<b>Customer / Bill To:</b><br/>Nordic Energy AS<br/>Fjordveien 45<br/>0150 Oslo, Norway", styles['Normal']),
            Paragraph("<b>Payment Terms:</b><br/>Net 30 Days<br/>IBAN: DE89370400440532013000", styles['Normal'])
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
        ["IoT Vibration Sensors (Industrial Grade)", "20", "EUR 150.00", "EUR 3,000.00"],
        ["Gateway Concentrator Units (LoRaWAN)", "5", "EUR 300.00", "EUR 1,500.00"],
        ["Subtotal", "", "", "EUR 4,500.00"],
        ["Tax (19% VAT)", "", "", "EUR 855.00"],
        ["Freight / Shipping Charges", "", "", "EUR 120.00"],
        ["Discount", "", "", "-EUR 200.00"],
        ["Total Amount Due", "", "", "EUR 5,275.00"],
    ]

    items_table = Table(items_data, colWidths=[310, 60, 85, 85])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (1, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, 2), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0, 3), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F1F5F9')),
        ('LINEABOVE', (0, 3), (-1, 3), 1, colors.HexColor('#0F172A')),
        ('LINEABOVE', (0, -1), (-1, -1), 1.5, colors.HexColor('#0F172A')),
    ]))
    story.append(items_table)
    doc.build(story)
    print(f"Created: {output_path}")

def create_airway_bol(output_path: str):
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
    story.append(Paragraph("AIR WAYBILL / MULTIMODAL BILL OF LADING", title_style))
    story.append(Spacer(1, 10))

    parties_data = [
        [
            Paragraph("<b>Shipper / Exporter:</b><br/>Tokyo Microchips Corp<br/>3-2-1 Chiyoda-ku<br/>Tokyo 100-0001, Japan", styles['Normal']),
            Paragraph("<b>Air Waybill Number:</b> <b>AWB-772-9102834</b><br/><b>Shipment Date:</b> 2024-11-05<br/><b>Carrier:</b> Japan Cargo Airlines", styles['Normal'])
        ],
        [
            Paragraph("<b>Consignee:</b><br/>Munich Precision Instruments GmbH<br/>Leopoldstrasse 88<br/>80802 Munich, Germany", styles['Normal']),
            Paragraph("<b>Notify Party:</b><br/>Schenker Global Logistics Deutschland<br/>Email: notify-muc@schenker.example<br/>Tel: +49-89-5550123", styles['Normal'])
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
        ["Place of Receipt", "Airport of Loading", "Airport of Discharge", "Final Destination"],
        ["Narita Cargo Terminal", "Tokyo Narita Airport (NRT)", "Munich Airport (MUC)", "Munich, Germany"],
        ["Flight / Vessel", "Voyage Number", "Container / ULD Number", "Seal Number"],
        ["Boeing 777F", "JL8421", "AKE-99218-JL, AKE-99219-JL", "SEAL-JP-7701, SEAL-JP-7702"],
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
        ["12 Pallets", "High Precision Microcontrollers & Semiconductor Wafers\nHS Code: 8542.31\nTemp Controlled +15C to +25C", "1,240.50 KGS", "6.4 CBM"]
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
    create_consulting_invoice("samples/sample_invoice_consulting.pdf")
    create_international_invoice("samples/sample_invoice_international.pdf")
    create_sample_bol("samples/sample_bol.pdf")
    create_airway_bol("samples/sample_bol_airway.pdf")
    create_blank_pdf("samples/blank_sample.pdf")
