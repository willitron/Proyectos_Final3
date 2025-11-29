from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

class PDFGenerator:
    """Generador de reportes PDF profesionales para Instituto Ballivián"""
    
    def __init__(self, filename, title, logo_path='static/img/logo.png'):
        self.filename = filename
        self.title = title
        self.logo_path = logo_path
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=100,
            bottomMargin=50
        )
        self.elements = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetaInfo',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_RIGHT
        ))
    
    def _create_header(self, canvas, doc):
        canvas.saveState()
        
        # Logo
        if os.path.exists(self.logo_path):
            try:
                logo = Image(self.logo_path, width=1*inch, height=1*inch)
                logo.drawOn(canvas, 50, doc.height + doc.topMargin - 60)
            except:
                pass
        
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(130, doc.height + doc.topMargin - 20, "INSTITUTO BALLIVIÁN")
        
        canvas.setFont('Helvetica', 9)
        canvas.drawString(130, doc.height + doc.topMargin - 35, "Sistema de Gestión Académica")
        canvas.drawString(130, doc.height + doc.topMargin - 50, "La Paz - Bolivia")
        
        canvas.setStrokeColor(colors.HexColor('#1a237e'))
        canvas.setLineWidth(2)
        canvas.line(50, doc.height + doc.topMargin - 70, 
                   doc.width + 50, doc.height + doc.topMargin - 70)
        
        canvas.restoreState()
    
    def _create_footer(self, canvas, doc):
        canvas.saveState()
        
        canvas.setStrokeColor(colors.HexColor('#1a237e'))
        canvas.setLineWidth(1)
        canvas.line(50, 40, doc.width + 50, 40)
        
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        
        page_num = canvas.getPageNumber()
        text = f"Página {page_num}"
        canvas.drawRightString(doc.width + 50, 25, text)
        
        canvas.drawString(50, 25, "Instituto Ballivián - www.institutoballivian.edu.bo")
        
        canvas.restoreState()
    
    def add_metadata(self, generated_by, user_role=None, additional_info=None):
        
        now = datetime.now()
        fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
        
        metadata = [
            ["Generado por:", generated_by],
            ["Fecha:", now.strftime("%d/%m/%Y")],
            ["Hora:", now.strftime("%H:%M:%S")],
        ]
        
        if user_role:
            metadata.append(["Rol:", user_role])
        
        if additional_info:
            for key, value in additional_info.items():
                metadata.append([f"{key}:", str(value)])
        
        meta_table = Table(metadata, colWidths=[1.5*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a237e')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        self.elements.append(meta_table)
        self.elements.append(Spacer(1, 0.3*inch))
    
    def add_title(self, title=None):
        if title is None:
            title = self.title
        
        title_para = Paragraph(title, self.styles['CustomTitle'])
        self.elements.append(title_para)
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_section(self, section_title):
        section_para = Paragraph(section_title, self.styles['CustomHeading'])
        self.elements.append(section_para)
    
    def add_paragraph(self, text):
        para = Paragraph(text, self.styles['CustomBody'])
        self.elements.append(para)
        self.elements.append(Spacer(1, 0.1*inch))
    
    def add_table(self, data, col_widths=None, style_config=None):
        """
        
        if not data:
            return
        
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1a237e')),
            
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        if style_config:
            table_style.extend(style_config)
        
        table.setStyle(TableStyle(table_style))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_spacer(self, height=0.2):
        self.elements.append(Spacer(1, height*inch))
    
    def add_page_break(self):
        self.elements.append(PageBreak())
    
    def add_summary_box(self, summary_data):
        """
        
        data = []
        for key, value in summary_data.items():
            data.append([key, str(value)])
        
        summary_table = Table(data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8eaf6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a237e')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1a237e')),
        ]))
        
        self.elements.append(summary_table)
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_signature_section(self, signatures):
        
        self.add_spacer(0.5)
        
        data = []
        row = []
        for i, sig in enumerate(signatures):
            row.append("_" * 30)
            if (i + 1) % 2 == 0 or i == len(signatures) - 1:
                data.append(row)
                row = []
        
        if row:
            data.append(row)
        
        sig_table = Table(data, colWidths=[2.5*inch, 2.5*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        self.elements.append(sig_table)
        
        name_data = []
        name_row = []
        for i, sig in enumerate(signatures):
            name_row.append(sig)
            if (i + 1) % 2 == 0 or i == len(signatures) - 1:
                name_data.append(name_row)
                name_row = []
        
        if name_row:
            name_data.append(name_row)
        
        name_table = Table(name_data, colWidths=[2.5*inch, 2.5*inch])
        name_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a237e')),
        ]))
        
        self.elements.append(name_table)
    
    def build(self):
        self.doc.build(
            self.elements,
            onFirstPage=self._create_header,
            onLaterPages=self._create_header,
            canvasmaker=self._add_footer_canvas
        )
    
    def _add_footer_canvas(self, canvas, doc):
        canvas.saveState()
        self._create_footer(canvas, doc)
        canvas.restoreState()
        return canvas