from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

def date_fmt(dt):
    if isinstance(dt, datetime):
        return dt.strftime("%d-%b-%Y")
    elif isinstance(dt, str):
        return dt
    return ""

def build_patient_dashboard_pdf(patient: dict) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Header
    elements.append(Paragraph("Patient Medical Data", styles['Title']))
    elements.append(Spacer(1, 12))

    # Basic Info
    elements.append(Paragraph(f"Paciente: {patient.get('name', '')} {patient.get('last_name', '')}", styles['Heading2']))
    elements.append(Paragraph(f"Fecha de nacimiento: {patient.get('birth_date', '')}", styles['Normal']))
    elements.append(Paragraph(f"Edad: {patient.get('age', '')} años", styles['Normal']))
    elements.append(Paragraph(f"Documento: {patient.get('document', '')}", styles['Normal']))
    elements.append(Paragraph(f"Colesterol: {patient.get('cholesterol', '')} mg/dL", styles['Normal']))
    elements.append(Paragraph(f"Glucosa: {patient.get('glucose', '')} mg/dL", styles['Normal']))
    elements.append(Paragraph(f"Nivel de Actividad: {patient.get('activity_level', '')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Medical History
    elements.append(Paragraph("Historia Médica", styles['Heading3']))
    history = [
        {
            "Fecha": date_fmt(h.get("date")),
            "Descripción": h.get("description", ""),
            "Observaciones": h.get("notes", "")
        }
        for h in patient.get("medical_history", [])
    ]
    if history:
        table_data = [list(history[0].keys())] + [list(row.values()) for row in history]
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey),('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        elements.append(t)
    elements.append(Spacer(1, 12))

    # # Weight by Month
    # elements.append(Paragraph("Peso por Mes", styles['Heading3']))
    # weights = [
    #     {
    #         "Mes": w.get("month", ""),
    #         "Peso (kg)": w.get("value", "")
    #     }
    #     for w in patient.get("weight_by_month", [])
    # ]
    # if weights:
    #     table_data = [list(weights[0].keys())] + [list(row.values()) for row in weights]
    #     t = Table(table_data, repeatRows=1)
    #     t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey),('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
    #     elements.append(t)
    # elements.append(Spacer(1, 12))

    # Vital Signs
    elements.append(Paragraph("Signos Vitales", styles['Heading3']))
    vitals = [
        {
            "Fecha": date_fmt(v.get("datetime")),
            "Frecuencia Cardíaca": v.get("heart_rate", ""),
            "Peso": v.get("daily_weight", ""),
            "Presión Arterial": f"{v.get('blood_pressure', {}).get('systolic', '')}/{v.get('blood_pressure', {}).get('diastolic', '')}"
        }
        for v in patient.get("vital_signs", [])
    ]
    if vitals:
        table_data = [list(vitals[0].keys())] + [list(row.values()) for row in vitals]
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey),('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        elements.append(t)
    elements.append(Spacer(1, 12))

    # Medications & Conditions
    elements.append(Paragraph("Medicamentos Prescritos:", styles['Heading3']))
    meds = patient.get("medications", [])
    elements.append(Paragraph(", ".join(meds), styles['Normal']))
    elements.append(Paragraph("Condiciones Preexistentes:", styles['Heading3']))
    conds = patient.get("conditions", [])
    elements.append(Paragraph(", ".join(conds), styles['Normal']))
    elements.append(Spacer(1, 12))

    # Hygiene Logs
    elements.append(Paragraph("Registro de Higiene", styles['Heading3']))
    hygiene = [
        {
            "Fecha": date_fmt(h.get("datetime")),
            "Nivel de Asistencia": h.get("assistance_level", ""),
            "Condición": h.get("condition", ""),
            "Estado": h.get("status", "")
        }
        for h in patient.get("hygiene_logs", [])
    ]
    if hygiene:
        table_data = [list(hygiene[0].keys())] + [list(row.values()) for row in hygiene]
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey),('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        elements.append(t)
    elements.append(Spacer(1, 12))

    # Meals
    elements.append(Paragraph("Registro de Comidas", styles['Heading3']))
    meals = [
        {
            "Fecha": date_fmt(m.get("datetime")),
            "Descripción": m.get("description", ""),
            "Hidratación": m.get("hydration", ""),
            "Comida": m.get("meal_type", ""),
            "Observaciones": m.get("observations", "")
        }
        for m in patient.get("meals", [])
    ]
    if meals:
        table_data = [list(meals[0].keys())] + [list(row.values()) for row in meals]
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey),('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        elements.append(t)
    elements.append(Spacer(1, 12))

    # Medication Logs
    elements.append(Paragraph("Registro de Medicación", styles['Heading3']))
    medlogs = [
        {
            "Fecha": date_fmt(m.get("datetime")),
            "Dosis": m.get("dose", ""),
            "Medicamento": m.get("medication_name", ""),
            "Vía de Administración": m.get("route", ""),
            "Estado": m.get("status", ""),
            "Observaciones": m.get("observations", "")
        }
        for m in patient.get("medication_logs", [])
    ]
    if medlogs:
        table_data = [list(medlogs[0].keys())] + [list(row.values()) for row in medlogs]
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey),('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        elements.append(t)
    elements.append(Spacer(1, 12))

    # Symptoms
    elements.append(Paragraph("Eventos de Salud", styles['Heading3']))
    symptoms = [
        {
            "Fecha": date_fmt(s.get("datetime")),
            "Descripción": s.get("description", ""),
            "Observaciones": s.get("observations", "")
        }
        for s in patient.get("symptoms", [])
    ]
    if symptoms:
        table_data = [list(symptoms[0].keys())] + [list(row.values()) for row in symptoms]
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey),('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        elements.append(t)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
