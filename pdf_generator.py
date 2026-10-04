import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from models import CompanyData

def generate_pdf(data: CompanyData, output_filename: str):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    elements = []
    
    # Title
    elements.append(Paragraph(f"Guptchar Report: {data.company_name}", title_style))
    elements.append(Spacer(1, 12))
    
    # Company Info
    elements.append(Paragraph("<b>Company Overview</b>", subtitle_style))
    elements.append(Paragraph(f"<b>Address:</b> {data.address}", normal_style))
    elements.append(Paragraph(f"<b>Website:</b> <a href='{data.website}'>{data.website}</a>", normal_style))
    elements.append(Paragraph(f"<b>Generic Phone:</b> {data.generic_contact_number}", normal_style))
    elements.append(Paragraph(f"<b>Primary Email:</b> {data.primary_email}", normal_style))
    elements.append(Paragraph(f"<b>Description:</b> {data.one_sentence_description}", normal_style))
    elements.append(Spacer(1, 12))
    
    # Executives Table
    elements.append(Paragraph("<b>Key Executives & Contacts</b>", subtitle_style))
    elements.append(Spacer(1, 6))
    
    if data.executives_and_contacts:
        table_data = [["Name", "Title", "Phone", "Email", "Source"]]
        for exec_contact in data.executives_and_contacts:
            table_data.append([
                exec_contact.name,
                exec_contact.title,
                exec_contact.phone,
                exec_contact.email,
                exec_contact.source
            ])
            
        t = Table(table_data, colWidths=[100, 100, 100, 120, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No executive contacts found.", normal_style))
        
    doc.build(elements)
    print(f"[*] PDF generated successfully: {output_filename}")
