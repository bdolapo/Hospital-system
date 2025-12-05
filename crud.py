# backend/crud.py
from sqlmodel import select
from sqlmodel import Session
from .models import Patient, Doctor, Appointment

# NOTE: sessions are created in streamlit app using engine sessionmaker pattern
# But these helpers accept an active Session.

# Patients
def create_patient(session: Session, patient: Patient) -> Patient:
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient

def list_patients(session: Session):
    return session.exec(select(Patient).order_by(Patient.created_at.desc())).all()

def get_patient(session: Session, patient_id: int):
    return session.get(Patient, patient_id)

def delete_patient(session: Session, patient_id: int):
    p = session.get(Patient, patient_id)
    if p:
        session.delete(p)
        session.commit()
    return p

# Doctors
def create_doctor(session: Session, doctor: Doctor) -> Doctor:
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor

def list_doctors(session: Session):
    return session.exec(select(Doctor).order_by(Doctor.name)).all()

# Appointments
def create_appointment(session: Session, appt: Appointment) -> Appointment:
    session.add(appt)
    session.commit()
    session.refresh(appt)
    return appt

def list_appointments(session: Session):
    return session.exec(select(Appointment).order_by(Appointment.date.desc())).all()

def list_appointments_for_patient(session: Session, patient_id: int):
    return session.exec(select(Appointment).where(Appointment.patient_id == patient_id).order_by(Appointment.date.desc())).all()
