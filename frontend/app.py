import streamlit as st
import requests
from datetime import date, time

BACKEND_URL = "http://localhost:8000/submit"

st.set_page_config(page_title="Formulário de Serviço Médico", layout="centered")

st.title("🩺 Formulário de Registro de Serviço Médico")

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
    medical_history = st.text_area("Histórico medical")

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

    response = requests.post(BACKEND_URL, json=payload)

    if response.status_code == 200:
        st.success("Data sent successfully!")
        st.download_button(
            "📄 Download PDF",
            data=response.content,
            file_name="medical_service_report.pdf",
            mime="application/pdf",
        )
    else:
        st.error("Failed to submit data")
