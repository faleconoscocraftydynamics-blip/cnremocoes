# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO


# def generate_pdf(data: dict) -> bytes:
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = []

#     elements.append(Paragraph("<b>Medical Service Report</b>", styles["Title"]))
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph(f"<b>Date:</b> {data['date']}", styles["Normal"]))
#     elements.append(Paragraph(f"<b>Time:</b> {data['time']}", styles["Normal"]))
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph("<b>Timestamps</b>", styles["Heading2"]))
#     for k, v in data["timestamps"].items():
#         elements.append(Paragraph(f"{k.capitalize()}: {v}", styles["Normal"]))

#     elements.append(Spacer(1, 12))
#     elements.append(Paragraph("<b>Kilometers</b>", styles["Heading2"]))
#     for k, v in data["kilometers"].items():
#         elements.append(Paragraph(f"{k.capitalize()}: {v} km", styles["Normal"]))

#     elements.append(Spacer(1, 12))
#     elements.append(Paragraph(f"<b>Service Type:</b> {data['service_type']}", styles["Normal"]))
#     elements.append(Paragraph(f"<b>Diagnostic:</b> {data['diagnostic']}", styles["Normal"]))

#     elements.append(Spacer(1, 12))
#     elements.append(Paragraph("<b>Patient Information</b>", styles["Heading2"]))
#     patient = data["patient"]

#     elements.append(Paragraph(f"Name: {patient['name']}", styles["Normal"]))
#     elements.append(Paragraph(f"Age: {patient['age']}", styles["Normal"]))
#     elements.append(Paragraph(f"Sex: {patient['sex']}", styles["Normal"]))
#     elements.append(Paragraph(f"Address: {patient['address']}", styles["Normal"]))
#     elements.append(Paragraph(f"Medical History: {patient['medical_history']}", styles["Normal"]))

#     doc.build(elements)
#     pdf = buffer.getvalue()
#     buffer.close()

#     return pdf

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


styles = getSampleStyleSheet()

WRAP_STYLE = ParagraphStyle(
    "WrapStyle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10,
    leading=14,
    spaceAfter=6,
)

def section_title(title):
    return Table(
        [[Paragraph(f"<b>{title}</b>", styles["Normal"])]],
        colWidths=[500],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 8),
        ],
    )


def key_value_table(data, col_widths=(150, 350)):
    table_data = []

    for key, value in data:
        if isinstance(value, str):
            value = Paragraph(value, WRAP_STYLE)

        table_data.append(
            [
                Paragraph(f"<b>{key}</b>", styles["Normal"]),
                value,
            ]
        )

    return Table(
        table_data,
        colWidths=col_widths,
        style=[
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ],
    )


def generate_pdf(data: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    elements = []

    # ─── HEADER ───────────────────────────────────────────────
    elements.append(
        Table(
            [[Paragraph("<b>RELATÓRIO DE SERVIÇO MÉDICO</b>", styles["Title"])]],
            colWidths=[500],
        )
    )
    elements.append(Spacer(1, 12))

    # ─── DATE & TIME ──────────────────────────────────────────
    elements.append(section_title("Data & Hora"))
    elements.append(
        key_value_table(
            [
                ("Data", data["date"]),
                ("Hora", data["time"]),
            ]
        )
    )
    elements.append(Spacer(1, 12))

    # ─── TIMESTAMPS ───────────────────────────────────────────
    elements.append(section_title("Timestamps"))
    elements.append(
        key_value_table(
            [
                ("Entrada", data["timestamps"]["entry"]),
                ("Saída", data["timestamps"]["exit"]),
                ("Chegada no destino", data["timestamps"]["arrival"]),
            ]
        )
    )
    elements.append(Spacer(1, 12))

    # ─── KILOMETERS ───────────────────────────────────────────
    elements.append(section_title("Kilometers"))
    elements.append(
        key_value_table(
            [
                ("KM at Entry", f"{data['kilometers']['entry']} km"),
                ("KM at Exit", f"{data['kilometers']['exit']} km"),
                ("KM at Arrival", f"{data['kilometers']['arrival']} km"),
            ]
        )
    )
    elements.append(Spacer(1, 12))

    # ─── SERVICE DETAILS ──────────────────────────────────────
    elements.append(section_title("Service Details"))
    elements.append(
        key_value_table(
            [
                ("Type of Service", data["service_type"]),
                ("Diagnostic", Paragraph(data["diagnostic"], WRAP_STYLE)),
            ]
        )
    )
    elements.append(Spacer(1, 12))

    # ─── PATIENT INFORMATION ──────────────────────────────────
    patient = data["patient"]

    elements.append(section_title("Patient Information"))
    elements.append(
        key_value_table(
            [
                ("Name", patient["name"]),
                ("Age", str(patient["age"])),
                ("Sex", patient["sex"]),
                ("Address", patient["address"]),
                (
                    "Medical History",
                    Paragraph(patient["medical_history"], WRAP_STYLE),
                ),
            ]
        )
    )

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    return pdf
