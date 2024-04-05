from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReportGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.elements = []
        self.styles = getSampleStyleSheet()

    def add_heading(self, heading_text):
        heading = Paragraph(heading_text, self.styles['Heading2'])
        self.elements.append(heading)
        self.elements.append(Spacer(1, 12))

    def add_table(self, table_data, headers):
        data = [headers] + [[entry[h] for h in headers] for entry in table_data]
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Add this line to left align the data
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def generate(self):
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        doc.build(self.elements)

    def get_filepath(self):
        return self.filename
