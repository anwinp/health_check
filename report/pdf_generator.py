from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
from reportlab.lib.colors import blue
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFReportGenerator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.document = SimpleDocTemplate(filepath, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.elements = []

    def generate_report(self):
        self.add_first_page()
        self.document.build(self.elements)

    def add_first_page(self):
        # Title
        title_style = self.styles['Heading1']
        title_style.alignment = 1  # Center alignment
        self.elements.append(Paragraph("<u>DZS GLOBAL SERVICES AND SUPPORT</u>", title_style))
        self.elements.append(Spacer(1, 4))

        # GSS on a new line
        gss_style = ParagraphStyle(
            'GSSStyle',
            parent=self.styles['Heading1'],
            alignment=1,  # Center alignment
        )
        self.elements.append(Paragraph("(GSS)", gss_style))
        self.elements.append(Spacer(1, 12))

        subtitle_style = self.styles['Heading2']
        subtitle_style.alignment = 1  # Center alignment
        self.elements.append(Paragraph("HealthCheck Report for I3", subtitle_style))
        self.elements.append(Spacer(1, 12))

        olt_style = self.styles['Heading3']
        olt_style.alignment = 1  # Center alignment
        self.elements.append(Paragraph("OLT: 172.16.114.24", olt_style))
        self.elements.append(Spacer(1, 24))

        # Prepared For and Prepared By tables
        data = [
            ['PREPARED FOR:', 'CUSTOMER'],
            ['', 'Position'],
            ['', 'Company'],
            ['', 'Address'],
            ['', 'Contact Details'],
            ['PREPARED BY:', 'DZS Employee'],
            ['', 'Position'],
            ['', 'Global Services & Support'],
            ['', 'Company'],
            ['', 'Address'],
            ['', 'Contact Details'],
            ['DATE:', 'Date']
        ]

        table = Table(data, colWidths=[1.5 * inch, 4.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 10), colors.white),
            ('TEXTCOLOR', (0, 0), (0, 10), colors.black),
            ('ALIGN', (0, 0), (1, 11), 'LEFT'),
            ('FONTNAME', (0, 0), (0, 11), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (0, 11), 12),
        ]))
        self.elements.append(table)

    def get_filepath(self):
        return self.filepath


