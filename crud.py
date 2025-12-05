from sqlmodel import select
from . import models


def list_patients(session):
    return session.exec(select(models.Patient)).all()


def create_patient(session, name, age, phone, notes):
    new = models.Patient(name=name, age=age, phone=phone, notes=notes)
    session.add(new)
    session.commit()
    session.refresh(new)
    return new


def list_doctors(session):
    return session.exec(select(models.Doctor)).all()


def create_doctor(session, name, specialty, phone):
    new = models.Doctor(name=name, specialty=specialty, phone=phone)
    session.add(new)
    session.commit()
    session.refresh(new)
    return new


def list_appointments(session):
    return session.exec(select(models.Appointment)).all()


def create_appointment(session, patient_id, doctor_id, date, reason):
    new = models.Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        date=date,
        reason=reason
    )
    session.add(new)
    session.commit()
    session.refresh(new)
    return new
