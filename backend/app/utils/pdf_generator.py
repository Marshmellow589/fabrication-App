from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        # Add custom styles
        self.styles.add(ParagraphStyle(
            name='Header',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=6,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3
        ))
        
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=1,
            textColor=colors.white
        ))
        
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=1
        ))
    
    def generate_fitup_report(self, records: List[Dict[str, Any]], operator_data: Dict[str, str]) -> BytesIO:
        """Generate Fit-Up Inspection Report PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        
        elements = []
        
        # Header Section
        elements.append(Paragraph("Project - FIT UP INSPECTION REPORT", self.styles['Header']))
        elements.append(Spacer(1, 10))
        
        # Project and Location
        project_info = [
            [Paragraph("Project:", self.styles['SubHeader']), Paragraph(operator_data.get('project', ''), self.styles['SubHeader'])],
            [Paragraph("Location:", self.styles['SubHeader']), Paragraph(operator_data.get('location', ''), self.styles['SubHeader'])],
            [Paragraph("Date:", self.styles['SubHeader']), Paragraph(operator_data.get('date', datetime.now().strftime('%Y-%m-%d')), self.styles['SubHeader'])],
            [Paragraph("Report No:", self.styles['SubHeader']), Paragraph(operator_data.get('report_no', ''), self.styles['SubHeader'])],
            [Paragraph("Drawing No:", self.styles['SubHeader']), Paragraph(operator_data.get('drawing_no', ''), self.styles['SubHeader'])]
        ]
        
        project_table = Table(project_info, colWidths=[1.5*inch, 3*inch])
        project_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(project_table)
        elements.append(Spacer(1, 15))
        
        # Data Table
        table_data = []
        
        # Table Headers
        headers = [
            "S/NO", "LINE NO", "SPOOL NO", "JOINT NO", 
            "MATERIAL -A", "MATERIAL-B", "JOINT TYPE", 
            "THICKNESS", "RESULT", "REMARK"
        ]
        table_data.append([Paragraph(header, self.styles['TableHeader']) for header in headers])
        
        # Table Rows
        for i, record in enumerate(records, 1):
            material_a = f"{record.get('part1_grade', '')} {record.get('part1_size', '')}".strip()
            material_b = f"{record.get('part2_grade', '')} {record.get('part2_size', '')}".strip()
            
            row = [
                Paragraph(str(i), self.styles['TableCell']),
                Paragraph(str(record.get('line_no', '')), self.styles['TableCell']),
                Paragraph(str(record.get('spool_no', '')), self.styles['TableCell']),
                Paragraph(str(record.get('joint_no', '')), self.styles['TableCell']),
                Paragraph(material_a, self.styles['TableCell']),
                Paragraph(material_b, self.styles['TableCell']),
                Paragraph(str(record.get('joint_type', '')), self.styles['TableCell']),
                Paragraph(str(record.get('part1_thickness', '')), self.styles['TableCell']),
                Paragraph(str(record.get('fitup_result', '')).upper(), self.styles['TableCell']),
                Paragraph("", self.styles['TableCell'])  # Empty remark column
            ]
            table_data.append(row)
        
        # Create table with appropriate column widths
        col_widths = [0.4*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.5*inch, 1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch]
        data_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Table styling
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        data_table.setStyle(table_style)
        elements.append(data_table)
        elements.append(Spacer(1, 20))
        
        # Footer Section
        footer_data = [
            [Paragraph("INSPECTION BY", self.styles['SubHeader']), Paragraph(operator_data.get('inspector', ''), self.styles['SubHeader'])],
            [Paragraph("NAME /SIGNATURE", self.styles['SubHeader']), Paragraph("", self.styles['SubHeader'])],
            [Paragraph("DATE", self.styles['SubHeader']), Paragraph(operator_data.get('date', datetime.now().strftime('%Y-%m-%d')), self.styles['SubHeader'])]
        ]
        
        footer_table = Table(footer_data, colWidths=[1.5*inch, 3*inch])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(footer_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_final_inspection_report(self, records: List[Dict[str, Any]], operator_data: Dict[str, str]) -> BytesIO:
        """Generate Final Inspection Report PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        
        elements = []
        
        # Header Section
        elements.append(Paragraph("Project - Final Inspection", self.styles['Header']))
        elements.append(Spacer(1, 10))
        
        # Project and Location
        project_info = [
            [Paragraph("Project:", self.styles['SubHeader']), Paragraph(operator_data.get('project', ''), self.styles['SubHeader'])],
            [Paragraph("Location:", self.styles['SubHeader']), Paragraph(operator_data.get('location', ''), self.styles['SubHeader'])],
            [Paragraph("Date:", self.styles['SubHeader']), Paragraph(operator_data.get('date', datetime.now().strftime('%Y-%m-%d')), self.styles['SubHeader'])],
            [Paragraph("Report No:", self.styles['SubHeader']), Paragraph(operator_data.get('report_no', ''), self.styles['SubHeader'])],
            [Paragraph("Drawing No:", self.styles['SubHeader']), Paragraph(operator_data.get('drawing_no', ''), self.styles['SubHeader'])]
        ]
        
        project_table = Table(project_info, colWidths=[1.5*inch, 3*inch])
        project_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(project_table)
        elements.append(Spacer(1, 15))
        
        # Data Table
        table_data = []
        
        # Table Headers for Final Inspection
        headers = [
            "S/NO", "LINE NO", "SPOOL NO", "JOINT NO", 
            "MATERIAL -A", "MATERIAL-B", "JOINT TYPE", 
            "THICKNESS", "WPS", "WELDER", "RESULT"
        ]
        table_data.append([Paragraph(header, self.styles['TableHeader']) for header in headers])
        
        # Table Rows
        for i, record in enumerate(records, 1):
            material_a = f"{record.get('part1_grade', '')} {record.get('part1_size', '')}".strip()
            material_b = f"{record.get('part2_grade', '')} {record.get('part2_size', '')}".strip()
            
            row = [
                Paragraph(str(i), self.styles['TableCell']),
                Paragraph(str(record.get('line_no', '')), self.styles['TableCell']),
                Paragraph(str(record.get('spool_no', '')), self.styles['TableCell']),
                Paragraph(str(record.get('joint_no', '')), self.styles['TableCell']),
                Paragraph(material_a, self.styles['TableCell']),
                Paragraph(material_b, self.styles['TableCell']),
                Paragraph(str(record.get('joint_type', '')), self.styles['TableCell']),
                Paragraph(str(record.get('part1_thickness', '')), self.styles['TableCell']),
                Paragraph(str(record.get('wps_no', '')), self.styles['TableCell']),
                Paragraph(str(record.get('welder_no', '')), self.styles['TableCell']),
                Paragraph(str(record.get('final_result', '')).upper(), self.styles['TableCell'])
            ]
            table_data.append(row)
        
        # Create table with appropriate column widths
        col_widths = [0.4*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.8*inch, 0.8*inch, 0.8*inch]
        data_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Table styling
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        data_table.setStyle(table_style)
        elements.append(data_table)
        elements.append(Spacer(1, 20))
        
        # Footer Section
        footer_data = [
            [Paragraph("INSPECTION BY", self.styles['SubHeader']), Paragraph(operator_data.get('inspector', ''), self.styles['SubHeader'])],
            [Paragraph("NAME /SIGNATURE", self.styles['SubHeader']), Paragraph("", self.styles['SubHeader'])],
            [Paragraph("DATE", self.styles['SubHeader']), Paragraph(operator_data.get('date', datetime.now().strftime('%Y-%m-%d')), self.styles['SubHeader'])]
        ]
        
        footer_table = Table(footer_data, colWidths=[1.5*inch, 3*inch])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(footer_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

# Global instance
pdf_generator = PDFGenerator()
