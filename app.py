import streamlit as st
from datetime import date, time
from fpdf import FPDF
import io

# Streamlit setup
st.set_page_config(page_title="Formulário de Serviço Médico", layout="centered")
st.title("🩺 Formulário de Registro de Serviço Médico")

# Define PDF generation function
def generate_pdf(payload):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatório de Serviço Médico", ln=True, align="C")

    # Service details
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Data do Serviço: {payload['date']}", ln=True)
    pdf.cell(200, 10, f"Hora do Serviço: {payload['time']}", ln=True)
    pdf.cell(200, 10, f"Tipo de Serviço: {payload['service_type']}", ln=True)
    pdf.cell(200, 10, f"Diagnóstico: {payload['diagnostic']}", ln=True)

    # Time Stamps
    pdf.cell(200, 10, f"Hora de Entrada: {payload['timestamps']['entry']}", ln=True)
    pdf.cell(200, 10, f"Hora de Saída: {payload['timestamps']['exit']}", ln=True)
    pdf.cell(200, 10, f"Hora de Destino: {payload['timestamps']['arrival']}", ln=True)

    # Kilometers
    pdf.cell(200, 10, f"KM Entrada: {payload['kilometers']['entry']}", ln=True)
    pdf.cell(200, 10, f"KM Saída: {payload['kilometers']['exit']}", ln=True)
    pdf.cell(200, 10, f"KM Destino: {payload['kilometers']['arrival']}", ln=True)

    # Patient Information
    pdf.ln(10)
    pdf.cell(200, 10, f"Nome do Paciente: {payload['patient']['name']}", ln=True)
    pdf.cell(200, 10, f"Idade: {payload['patient']['age']}", ln=True)
    pdf.cell(200, 10, f"Sexo: {payload['patient']['sex']}", ln=True)
    pdf.cell(200, 10, f"Endereço: {payload['patient']['address']}", ln=True)
    pdf.multi_cell(0, 10, f"Histórico Médico: {payload['patient']['medical_history']}", align="L")

    # Save PDF to a binary stream (memory)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return pdf_output

# Form input
with st.form("medical_service_form"):
    st.subheader("1️⃣ Data e Hora")
    service_date = st.date_input("Data", value=date.today())
    service_time = st.time_input("Hora", value=time(8, 0))

    st.subheader("2️⃣ Hora")
    col1, col2, col3 = st.columns(3)
    with col1:
        entry_time = st.time_input("H. Entrada")
    with col2:
        exit_time = st.time_input("H. Saída")
    with col3:
        arrival_time = st.time_input("H. Destino")

    st.subheader("3️⃣ Kilometros")
    col1, col2, col3 = st.columns(3)
    with col1:
        km_entry = st.number_input("KM Entrada", min_value=0.0, step=0.1)
    with col2:
        km_exit = st.number_input("KM Saída", min_value=0.0, step=0.1)
    with col3:
        km_arrival = st.number_input("KM Destino", min_value=0.0, step=0.1)

    st.subheader("4️⃣ Informação de Serviço")
    service_type = st.selectbox(
        "Tipo de Serviço",
        [
            "Emergência",
            "Transporte agendado",
            "Consulta médica",
            "Transferência hospitalar",
            "Outros"
        ]
    )

    diagnostic = st.text_area("Diagnósticos")

    st.subheader("5️⃣ Informações do Paciente")
    patient_name = st.text_input("Nome")
    patient_age = st.number_input("Idade", min_value=0, max_value=120, step=1)
    patient_sex = st.selectbox("Sexo", ["Masculino", "Feminino"])

    patient_address = st.text_area("Endereço")
    medical_history = st.text_area("Histórico médico")

    submitted = st.form_submit_button("✅ Enviar")

if submitted:
    st.success("Formulário enviado com sucesso!")

    payload = {
        "date": str(service_date),
        "time": str(service_time),
        "timestamps": {
            "entry": str(entry_time),
            "exit": str(exit_time),
            "arrival": str(arrival_time),
        },
        "kilometers": {
            "entry": km_entry,
            "exit": km_exit,
            "arrival": km_arrival,
        },
        "service_type": service_type,
        "diagnostic": diagnostic,
        "patient": {
            "name": patient_name,
            "age": patient_age,
            "sex": patient_sex,
            "address": patient_address,
            "medical_history": medical_history,
        },
    }

    # Generate PDF from the input data
    pdf_output = generate_pdf(payload)

    # Allow the user to download the generated PDF
    st.download_button(
        "📄 Baixar PDF",
        data=pdf_output,
        file_name="relatorio_servico_medico.pdf",
        mime="application/pdf",
    )
