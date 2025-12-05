import streamlit as st
from db import create_db_and_tables, get_session
import crud as crud

st.set_page_config(page_title="Hospital System", page_icon="🏥", layout="wide")

# Create DB
create_db_and_tables()

st.title("🏥 Hospital Management System")
st.write("A colorful Streamlit-first demo. Create patients, doctors and appointments.")


# ---- Sidebar Navigation ----
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Patients", "Doctors", "Appointments"])


# ---- DASHBOARD ----
if page == "Dashboard":
    st.header("📊 Dashboard")

    with next(get_session()) as s:
        pcount = len(crud.list_patients(s))
        dcount = len(crud.list_doctors(s))
        acount = len(crud.list_appointments(s))

    st.metric("Total Patients", pcount)
    st.metric("Total Doctors", dcount)
    st.metric("Appointments", acount)


# ---- PATIENTS ----
elif page == "Patients":
    st.header("🧑‍⚕️ Patients")

    with next(get_session()) as s:
        patients = crud.list_patients(s)

    st.subheader("Add new patient")

    with st.form("patient_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        phone = st.text_input("Phone")
        notes = st.text_area("Notes")

        submit = st.form_submit_button("Add patient")

        if submit:
            with next(get_session()) as s:
                crud.create_patient(s, name, age, phone, notes)
            st.success("Patient added!")
            st.rerun()

    st.subheader("Patient List")
    st.table(patients)


# ---- DOCTORS ----
elif page == "Doctors":
    st.header("🩺 Doctors")

    with next(get_session()) as s:
        doctors = crud.list_doctors(s)

    st.subheader("Add new doctor")

    with st.form("doctor_form"):
        name = st.text_input("Name")
        specialty = st.text_input("Specialty")
        phone = st.text_input("Phone")

        submit = st.form_submit_button("Add doctor")

        if submit:
            with next(get_session()) as s:
                crud.create_doctor(s, name, specialty, phone)
            st.success("Doctor added!")
            st.rerun()

    st.subheader("Doctors List")
    st.table(doctors)


# ---- APPOINTMENTS ----
elif page == "Appointments":
    st.header("📅 Appointments")

    with next(get_session()) as s:
        patients = crud.list_patients(s)
        doctors = crud.list_doctors(s)
        appointments = crud.list_appointments(s)

    st.subheader("Book appointment")

    with st.form("appoint_form"):
        patient = st.selectbox("Patient", patients, format_func=lambda x: x.name)
        doctor = st.selectbox("Doctor", doctors, format_func=lambda x: x.name)
        date = st.date_input("Date")
        reason = st.text_area("Reason")

        submit = st.form_submit_button("Book")

        if submit:
            with next(get_session()) as s:
                crud.create_appointment(s, patient.id, doctor.id, str(date), reason)
            st.success("Appointment booked")
            st.rerun()

    st.subheader("Appointments List")
    st.table(appointments)
