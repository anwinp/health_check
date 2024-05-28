

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, Inches, Cm

class WordReportGenerator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.document = Document()

    def set_font(self, run, font_name, size, bold=False, underline=False):
        run.font.name = font_name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
        run.font.size = Pt(size)
        run.bold = bold
        if underline:
            run.underline = True

    def remove_table_borders(self, table):
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._element.get_or_add_tcPr()
                tcBorders = tcPr.find(qn('w:tcBorders'))
                if tcBorders is None:
                    tcBorders = OxmlElement('w:tcBorders')
                    tcPr.append(tcBorders)
                for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                    border = tcBorders.find(qn(f'w:{border_name}'))
                    if border is None:
                        border = OxmlElement(f'w:{border_name}')
                        tcBorders.append(border)
                    border.set(qn('w:val'), 'none')

    def set_column_widths(self, table, widths):
        for row in table.rows:
            for idx, width in enumerate(widths):
                row.cells[idx].width = width

    def add_first_page(self):
        # Add title with Corbel font, size 26, and underline
        title = self.document.add_heading(level=1)
        title_run = title.add_run('DZS GLOBAL SERVICES AND SUPPORT')
        self.set_font(title_run, 'Corbel', 24, underline=True)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Add subtitle (GSS) as heading1
        subtitle = self.document.add_heading(level=1)
        subtitle_run = subtitle.add_run('(GSS)')
        self.set_font(subtitle_run, 'Corbel', 26)
        subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Add report title
        report_title = self.document.add_paragraph()
        report_title_run = report_title.add_run('HealthCheck Report for I3')
        self.set_font(report_title_run, 'Segoe UI', 20, bold=True)
        report_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Add OLT
        olt = self.document.add_paragraph()
        olt_run = olt.add_run('OLT: 172.16.114.24')
        self.set_font(olt_run, 'Segoe UI', 20, bold=True)
        olt.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Add space
        self.document.add_paragraph()

        # Create a table with 2 columns and 5 rows for PREPARED FOR
        table1 = self.document.add_table(rows=5, cols=2)
        self.remove_table_borders(table1)
        self.set_column_widths(table1, [Inches(1.5), Inches(4.5)])

        # Fill in the first table
        table1.cell(0, 0).text = 'PREPARED FOR:'
        prepared_for_run = table1.cell(0, 0).paragraphs[0].runs[0]
        self.set_font(prepared_for_run, 'Segoe UI', 12, bold=True)

        table1.cell(0, 1).text = 'CUSTOMER'
        customer_run = table1.cell(0, 1).paragraphs[0].runs[0]
        self.set_font(customer_run, 'Segoe UI', 12, bold=True)

        table1.cell(1, 1).text = 'Position'
        position_run = table1.cell(1, 1).paragraphs[0].runs[0]
        self.set_font(position_run, 'Segoe UI', 12)

        table1.cell(2, 1).text = 'Company'
        company_run = table1.cell(2, 1).paragraphs[0].runs[0]
        self.set_font(company_run, 'Segoe UI', 12)

        table1.cell(3, 1).text = 'Address'
        address_run = table1.cell(3, 1).paragraphs[0].runs[0]
        self.set_font(address_run, 'Segoe UI', 12)

        table1.cell(4, 1).text = 'Contact Details'
        contact_run = table1.cell(4, 1).paragraphs[0].runs[0]
        self.set_font(contact_run, 'Segoe UI', 12)

        # Add space
        self.document.add_paragraph()

        # Create a table with 2 columns and 6 rows for PREPARED BY
        table2 = self.document.add_table(rows=6, cols=2)
        self.remove_table_borders(table2)
        self.set_column_widths(table2, [Inches(1.5), Inches(4.5)])

        # Fill in the second table
        table2.cell(0, 0).text = 'PREPARED BY:'
        prepared_by_run = table2.cell(0, 0).paragraphs[0].runs[0]
        self.set_font(prepared_by_run, 'Segoe UI', 12, bold=True)

        table2.cell(0, 1).text = 'DZS Employee'
        dzs_employee_run = table2.cell(0, 1).paragraphs[0].runs[0]
        self.set_font(dzs_employee_run, 'Segoe UI', 12, bold=True)

        table2.cell(1, 1).text = 'Position'
        position_run_by = table2.cell(1, 1).paragraphs[0].runs[0]
        self.set_font(position_run_by, 'Segoe UI', 12)

        table2.cell(2, 1).text = 'Global Services & Support'
        gss_run = table2.cell(2, 1).paragraphs[0].runs[0]
        self.set_font(gss_run, 'Segoe UI', 12)

        table2.cell(3, 1).text = 'Company'
        company_run_by = table2.cell(3, 1).paragraphs[0].runs[0]
        self.set_font(company_run_by, 'Segoe UI', 12)

        table2.cell(4, 1).text = 'Address'
        address_run_by = table2.cell(4, 1).paragraphs[0].runs[0]
        self.set_font(address_run_by, 'Segoe UI', 12)

        table2.cell(5, 1).text = 'Contact Details'
        contact_run_by = table2.cell(5, 1).paragraphs[0].runs[0]
        self.set_font(contact_run_by, 'Segoe UI', 12)

        # Add space
        self.document.add_paragraph()

        # Add Date section
        date = self.document.add_paragraph()
        date.add_run('DATE: ').bold = True
        date_run = date.add_run('Date')
        self.set_font(date_run, 'Segoe UI', 12)

    def add_table_of_contents(self):
        # Add a page break
        self.document.add_page_break()

        # Add TOC heading
        toc_heading = self.document.add_heading('TABLE OF CONTENTS', level=1)
        toc_heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Add TOC entries
        toc_entries = [
            ('1.0 Executive Summary', 3),
            ('2.0 Overview', 4),
            ('3.0 System summary', 5),
            ('4.0 Card summary', 6),
            ('5.0 Port summary', 7),
            ('6.0 Log & Alarm analysis', 8),
            ('7.0 Stats and KPI analysis', 9),
            ('8.0 ONT analysis', 10),
            ('9.0 Final analysis and next steps', 11),
        ]

        for entry, page_number in toc_entries:
            paragraph = self.document.add_paragraph()
            run = paragraph.add_run(entry)
            self.set_font(run, 'Segoe UI', 12)
            tab_stop = paragraph.paragraph_format.tab_stops.add_tab_stop(Cm(16))
            paragraph.add_run('\t')
            run_page = paragraph.add_run(str(page_number))
            self.set_font(run_page, 'Segoe UI', 12)
            paragraph.paragraph_format.tab_stops.clear_all()

    def add_content_sections(self):
        # Add sections for each TOC entry
        section_titles = [
            '1.0 Executive Summary',
            '2.0 Overview',
            '3.0 System summary',
            '4.0 Card summary',
            '5.0 Port summary',
            '6.0 Log & Alarm analysis',
            '7.0 Stats and KPI analysis',
            '8.0 ONT analysis',
            '9.0 Final analysis and next steps',
        ]

        for title in section_titles:
            self.document.add_page_break()
            heading = self.document.add_heading(level=1)
            run = heading.add_run(title)
            self.set_font(run, 'Segoe UI', 20)
            # Add some placeholder text
            paragraph = self.document.add_paragraph('Content for ' + title)
            self.set_font(paragraph.add_run(), 'Segoe UI', 12)

    def generate_report(self):
        self.add_first_page()
        self.add_table_of_contents()
        self.add_content_sections()
        self.document.save(self.filepath)

    def get_filepath(self):
        return self.filepath