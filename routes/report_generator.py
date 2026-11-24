"""
EduPredict PDF Academic Report Generator
Generates clean, professional PDF reports using ReportLab with purple brand identity styling.
"""

import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_student_pdf_report(student, analytics, marks_list, feedback_list, parent_name=None) -> io.BytesIO:
    """
    Builds a complete, formatted PDF progress report.
    Returns an in-memory BytesIO buffer ready for send_file().
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles in Purple / Indigo brand theme
    brand_primary = colors.HexColor("#7C3AED")
    brand_dark = colors.HexColor("#4C1D95")
    brand_bg = colors.HexColor("#F5F3FF")
    text_main = colors.HexColor("#1E1B4B")
    status_green = colors.HexColor("#16A34A")
    status_orange = colors.HexColor("#F59E0B")
    status_red = colors.HexColor("#DC2626")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=brand_dark
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=brand_primary
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=brand_dark,
        spaceAfter=6
    )
    normal_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=text_main
    )
    bold_style = ParagraphStyle(
        "BodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=text_main
    )

    elements = []

    # 1. Header with Logo & Brand
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images", "edupredict-logo.png")
    
    header_data = []
    if os.path.exists(logo_path):
        img = Image(logo_path, width=2.0 * inch, height=0.75 * inch)
        header_data = [
            [img, Paragraph("<b>EduPredict</b><br><font color='#7C3AED'>Predict. Perform. Progress.</font><br><font size=7 color='#666'>Official Student Academic Performance & AI Evaluation Report</font>", normal_style)]
        ]
    else:
        header_data = [
            [Paragraph("<b>EduPredict</b>", title_style), Paragraph("<font color='#7C3AED'>Predict. Perform. Progress.</font><br>Academic Performance Evaluation", subtitle_style)]
        ]

    header_table = Table(header_data, colWidths=[2.2 * inch, 5.0 * inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=2, color=brand_primary, spaceBefore=4, spaceAfter=14))

    # 2. Student Particulars Card
    parent_line = f"<b>Parent / Guardian:</b> {parent_name}" if parent_name else "<b>Report Type:</b> Comprehensive Semester Evaluation"
    particulars_data = [
        [Paragraph(f"<b>Student Name:</b> {student.full_name}", normal_style), Paragraph(f"<b>Student ID:</b> {student.student_id}", normal_style)],
        [Paragraph(f"<b>Class / Section:</b> {student.class_grade}", normal_style), Paragraph(f"<b>Department:</b> {student.department.name if student.department else 'N/A'}", normal_style)],
        [Paragraph(f"<b>Semester:</b> {student.semester.name if student.semester else 'Current'}", normal_style), Paragraph(parent_line, normal_style)],
        [Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y - %I:%M %p')}", normal_style), Paragraph(f"<b>Status:</b> Active Academic Standing", normal_style)]
    ]
    part_table = Table(particulars_data, colWidths=[3.6 * inch, 3.6 * inch])
    part_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), brand_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#DDD6FE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EDE9FE")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(part_table)
    elements.append(Spacer(1, 14))

    # 3. AI Predictive Trajectory Box
    risk = analytics.get("risk_level", "Low")
    risk_color = status_green if risk == "Low" else (status_orange if risk == "Medium" else status_red)

    ai_data = [
        [
            Paragraph("<b>Predicted Academic Score</b>", bold_style),
            Paragraph("<b>Performance Category</b>", bold_style),
            Paragraph("<b>Risk Level</b>", bold_style)
        ],
        [
            Paragraph(f"<font size=16 color='#7C3AED'><b>{analytics.get('predicted_score')}%</b></font>", normal_style),
            Paragraph(f"<font size=12><b>{analytics.get('performance_category')}</b></font>", normal_style),
            Paragraph(f"<font size=12 color='{risk_color.hexval()}'><b>{risk.upper()}</b></font>", normal_style)
        ]
    ]
    ai_table = Table(ai_data, colWidths=[2.4 * inch, 2.4 * inch, 2.4 * inch])
    ai_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDE9FE")),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BOX', (0,0), (-1,-1), 1.5, brand_primary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DDD6FE")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(Paragraph("AI-Powered Academic Trajectory & Early Risk Forecast", heading_style))
    elements.append(ai_table)
    elements.append(Spacer(1, 14))

    # 4. Attendance & Coursework Summary
    att_pct = analytics.get("attendance_pct", 0)
    att_status = "Meeting Benchmark (≥75%)" if att_pct >= 75.0 else "Warning: Below 75% Requirement"
    att_color = status_green if att_pct >= 75.0 else status_red

    att_summary_data = [
        [Paragraph("<b>Metric</b>", bold_style), Paragraph("<b>Value</b>", bold_style), Paragraph("<b>Institutional Benchmark / Status</b>", bold_style)],
        [Paragraph("Classroom Attendance", normal_style), Paragraph(f"<b>{att_pct}%</b> ({analytics.get('attended_sessions')}/{analytics.get('total_sessions')} sessions)", normal_style), Paragraph(f"<font color='{att_color.hexval()}'><b>{att_status}</b></font>", normal_style)],
        [Paragraph("Internal Assessment Average", normal_style), Paragraph(f"<b>{analytics.get('avg_internal_pct')}%</b>", normal_style), Paragraph("Continuous assessment average across subjects", normal_style)],
        [Paragraph("Assignment Completion", normal_style), Paragraph(f"<b>{analytics.get('assignment_pct')}%</b> ({analytics.get('completed_assignments')}/{analytics.get('total_assignments')} completed)", normal_style), Paragraph("Coursework submissions", normal_style)],
    ]
    att_table = Table(att_summary_data, colWidths=[2.2 * inch, 2.2 * inch, 2.8 * inch])
    att_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F3F4F6")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(Paragraph("Attendance & Coursework Key Indicators", heading_style))
    elements.append(att_table)
    elements.append(Spacer(1, 14))

    # 5. Subject-Wise Examination Marks
    elements.append(Paragraph("Continuous Examination Marks Breakdown", heading_style))
    if marks_list:
        marks_table_data = [
            [Paragraph("<b>Subject Code</b>", bold_style), Paragraph("<b>Subject Name</b>", bold_style), Paragraph("<b>Exam Type</b>", bold_style), Paragraph("<b>Marks</b>", bold_style), Paragraph("<b>Percentage</b>", bold_style)]
        ]
        for m in marks_list[:8]:
            pct = round((float(m.marks_obtained) / float(m.max_marks)) * 100, 1)
            sub_code = m.subject.code if m.subject else "GEN"
            sub_name = m.subject.name if m.subject else "General Subject"
            marks_table_data.append([
                Paragraph(sub_code, normal_style),
                Paragraph(sub_name, normal_style),
                Paragraph(m.exam_type, normal_style),
                Paragraph(f"{m.marks_obtained} / {m.max_marks}", normal_style),
                Paragraph(f"<b>{pct}%</b>", normal_style)
            ])
        m_table = Table(marks_table_data, colWidths=[1.1 * inch, 2.6 * inch, 1.5 * inch, 1.0 * inch, 1.0 * inch])
        m_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F3F4F6")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(m_table)
    else:
        elements.append(Paragraph("<i>No formal examination marks recorded yet.</i>", normal_style))

    elements.append(Spacer(1, 14))

    # 6. Personalized Pedagogical Recommendations
    elements.append(Paragraph("Personalized Improvement Recommendations", heading_style))
    recs = analytics.get("recommendations", [])
    if recs:
        rec_items = []
        for r in recs:
            rec_items.append([Paragraph(f"&bull; {r}", normal_style)])
        r_table = Table(rec_items, colWidths=[7.2 * inch])
        r_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), brand_bg),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#DDD6FE")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(r_table)

    # 7. Official Institutional Sign-Off
    elements.append(Spacer(1, 22))
    sign_data = [
        [Paragraph("<b>Faculty In-Charge Signature:</b> ____________________", normal_style),
         Paragraph("<b>Institutional Seal & Verification:</b> ____________________", normal_style)]
    ]
    sign_table = Table(sign_data, colWidths=[3.6 * inch, 3.6 * inch])
    sign_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(KeepTogether([sign_table]))

    doc.build(elements)
    buffer.seek(0)
    return buffer
