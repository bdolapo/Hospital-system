from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    gender: str
    condition: str
    admission_date: datetime = Field(default_factory=datetime.utcnow)


class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    specialization: str
    years_experience: int


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")
    date: datetime
    notes: str
