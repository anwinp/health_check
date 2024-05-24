# report_data/views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import io

def generate_health_check_report(request):
    # Create a byte stream buffer
    buffer = io.BytesIO()

    # Create a SimpleDocTemplate with the buffer
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("HealthCheck Report for I3", styles['Title']))
    story.append(Spacer(1, 12))

    # Prepared For Section
    story.append(Paragraph("<b>Prepared For:</b> CUSTOMER", styles['Normal']))
    story.append(Paragraph("Position", styles['Normal']))
    story.append(Paragraph("Company", styles['Normal']))
    story.append(Paragraph("Address", styles['Normal']))
    story.append(Paragraph("Contact Details", styles['Normal']))
    story.append(Spacer(1, 12))

    # Prepared By Section
    story.append(Paragraph("<b>Prepared By:</b> DZS Employee", styles['Normal']))
    story.append(Paragraph("Position", styles['Normal']))
    story.append(Paragraph("Global Services & Support", styles['Normal']))
    story.append(Paragraph("Company", styles['Normal']))
    story.append(Paragraph("Address", styles['Normal']))
    story.append(Paragraph("Contact Details", styles['Normal']))
    story.append(Spacer(1, 12))

    # Date
    story.append(Paragraph("DATE: Date", styles['Normal']))
    story.append(Spacer(1, 12))

    # Table of Contents
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", styles['Heading1']))
    toc_data = [
        ['1.0 Executive Summary', '3'],
        ['2.0 Overview', '4'],
        ['3.0 System summary', '5'],
        ['4.0 Card summary', '6'],
        ['5.0 Port summary', '7'],
        ['6.0 Log & Alarm analysis', '8'],
        ['7.0 Stats and KPI analysis', '9'],
        ['8.0 ONT analysis', '10'],
        ['9.0 Final analysis and next steps', '11'],
    ]
    table = Table(toc_data, colWidths=[400, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # Executive Summary Section
    story.append(Paragraph("<b>1.0 EXECUTIVE SUMMARY</b>", styles['Heading1']))
    story.append(Paragraph("Need to provide an overall summary of this doc and purpose and what was done", styles['Normal']))
    story.append(Paragraph("Provide executive summary of the health check..similar to below slide, but in graphs (pie-chart or something).", styles['Normal']))
    story.append(Spacer(1, 12))

    # Build the PDF
    doc.build(story)

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="health_check_report.pdf"'
    response.write(pdf)
    return response
