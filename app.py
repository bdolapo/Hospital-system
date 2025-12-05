# frontend/streamlit_app.py
import streamlit as st
from sqlmodel import Session, select
from backend.db import create_db_and_tables, engine, get_session
from backend import models, crud
from datetime import datetime
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(".."))

from backend.database import create_db, get_session, engine
from backend.models import Patient, Doctor, Appointment

# ----- Page config -----
st.set_page_config(page_title="Hospital System", layout="wide", page_icon="🏥")

# ----- Ensure DB exists -----
create_db_and_tables()

# ----- Load CSS -----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = os.path.join("frontend", "assets.css")
if os.path.exists(css_path):
    local_css(css_path)

# ----- Helper: get DB session -----
def get_db():
    with Session(engine) as session:
        yield session

# ----- Sidebar navigation -----
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2965/2965567.png", width=60)
st.sidebar.title("🏥 Hospital")
menu = st.sidebar.radio("Go to", ["Overview", "Patients", "Doctors", "Appointments", "Reports"])

# ----- Overview -----
if menu == "Overview":
    st.markdown('<div class="app-header card grad-blue"><h1 style="margin:4px">🏥 Hospital Management</h1><p style="margin:2px">A colorful Streamlit-first hospital demo. Create patients, doctors and appointments.</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.8,1,1.2])
    with col1:
        st.markdown('<div class="card grad-green"><h3>Quick Actions</h3><ul><li>Create patient</li><li>Create doctor</li><li>Book appointment</li></ul></div>', unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown('<div class="card grad-orange"><h3>Tips</h3><p class="small">Deploy to Streamlit for free. Use GitHub to store your repo. Add authentication later.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card" style="background:#fff;"><h3>Stats</h3>', unsafe_allow_html=True)
        with Session(engine) as s:
            pcount = s.exec(select(models.Patient)).count()
            dcount = s.exec(select(models.Doctor)).count()
            acount = s.exec(select(models.Appointment)).count()
        st.metric("Patients", pcount, delta=None)
        st.metric("Doctors", dcount, delta=None)
        st.metric("Appointments", acount, delta=None)
        st.markdown("</div>", unsafe_allow_html=True)

# ----- Patients -----
if menu == "Patients":
    st.header("👩‍⚕️ Patients")
    left, right = st.columns([2,1])
    with left:
        with st.form("create_patient"):
            st.subheader("Create Patient")
            pname = st.text_input("Full name")
            page = st.number_input("Age", min_value=0, max_value=150, value=25)
            pphone = st.text_input("Phone")
            pnotes = st.text_area("Notes")
            if st.form_submit_button("Add patient"):
                patient = models.Patient(name=pname, age=page, phone=pphone, notes=pnotes)
                with Session(engine) as s:
                    crud.create_patient(s, patient)
                st.success("Patient created ✅")
    with right:
        st.subheader("Patients list")
        with Session(engine) as s:
            patients = crud.list_patients(s)
        if patients:
            df = pd.DataFrame([{"id":p.id,"name":p.name,"age":p.age,"phone":p.phone,"created":p.created_at} for p in patients])
            st.dataframe(df)
            sel = st.selectbox("Select patient for details", options=[(p.id,f"{p.name} (#{p.id})") for p in patients], format_func=lambda x: x[1] if isinstance(x, tuple) else x)
            if sel:
                pid = sel[0] if isinstance(sel, tuple) else sel
                with Session(engine) as s:
                    patient = crud.get_patient(s, int(pid))
                if patient:
                    st.markdown(f"**{patient.name}**  — Age: {patient.age}")
                    st.write("Notes:", patient.notes)
                    if st.button("Delete patient"):
                        with Session(engine) as s:
                            crud.delete_patient(s, int(pid))
                        st.success("Deleted ✅")
        else:
            st.info("No patients yet — create one!")

# ----- Doctors -----
if menu == "Doctors":
    st.header("🩺 Doctors")
    c1, c2 = st.columns(2)
    with c1:
        with st.form("create_doctor"):
            st.subheader("Create Doctor")
            dname = st.text_input("Name")
            dspec = st.text_input("Specialty")
            dphone = st.text_input("Phone")
            if st.form_submit_button("Add doctor"):
                doctor = models.Doctor(name=dname, specialty=dspec, phone=dphone)
                with Session(engine) as s:
                    crud.create_doctor(s, doctor)
                st.success("Doctor created ✅")
    with c2:
        st.subheader("Doctors list")
        with Session(engine) as s:
            doctors = crud.list_doctors(s)
        if doctors:
            df = pd.DataFrame([{"id":d.id,"name":d.name,"specialty":d.specialty,"phone":d.phone} for d in doctors])
            st.dataframe(df)
        else:
            st.info("No doctors yet.")

# ----- Appointments -----
if menu == "Appointments":
    st.header("📅 Appointments")
    left, right = st.columns([1.5,1])
    with left:
        with st.form("create_appointment"):
            st.subheader("Book Appointment")
            with Session(engine) as s:
                patients = crud.list_patients(s)
                doctors = crud.list_doctors(s)
            if not patients:
                st.warning("Create patients first.")
            if not doctors:
                st.warning("Create doctors first.")
            patient_map = {f"{p.name} (#{p.id})": p.id for p in patients}
            doctor_map = {f"{d.name} — {d.specialty} (#{d.id})": d.id for d in doctors}
            psel = st.selectbox("Patient", options=list(patient_map.keys())) if patients else None
            dsel = st.selectbox("Doctor", options=list(doctor_map.keys())) if doctors else None
            date = st.date_input("Date", value=datetime.today())
            time = st.time_input("Time", value=datetime.now().time())
            reason = st.text_input("Reason")
            if st.form_submit_button("Book"):
                if not (psel and dsel):
                    st.error("Choose both patient and doctor")
                else:
                    pid = patient_map[psel]
                    did = doctor_map[dsel]
                    dt = datetime.combine(date, time)
                    appt = models.Appointment(patient_id=pid, doctor_id=did, date=dt, reason=reason)
                    with Session(engine) as s:
                        crud.create_appointment(s, appt)
                    st.success("Appointment booked ✅")
    with right:
        st.subheader("Upcoming appointments")
        with Session(engine) as s:
            appts = crud.list_appointments(s)
        if appts:
            appt_rows = []
            for a in appts:
                # resolve patient & doctor names
                with Session(engine) as s:
                    p = s.get(models.Patient, a.patient_id)
                    d = s.get(models.Doctor, a.doctor_id)
                appt_rows.append({
                    "id": a.id,
                    "patient": p.name if p else "—",
                    "doctor": d.name if d else "—",
                    "date": a.date,
                    "status": a.status,
                    "reason": a.reason
                })
            df = pd.DataFrame(appt_rows)
            st.dataframe(df)
        else:
            st.info("No appointments yet.")

# ----- Reports -----
if menu == "Reports":
    st.header("📊 Reports")
    with Session(engine) as s:
        pats = crud.list_patients(s)
        docs = crud.list_doctors(s)
        appts = crud.list_appointments(s)
    st.metric("Patients", len(pats))
    st.metric("Doctors", len(docs))
    st.metric("Appointments", len(appts))
    if appts:
        df = pd.DataFrame([{"patient_id":a.patient_id,"doctor_id":a.doctor_id,"date":a.date,"status":a.status} for a in appts])
        st.bar_chart(df["patient_id"].value_counts())

