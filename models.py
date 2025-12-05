from sqlmodel import SQLModel, Field
from typing import Optional
import datetime


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    phone: str
    notes: Optional[str] = None


class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    specialty: str
    phone: str


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int
    doctor_id: int
    date: str
    reason: Optional[str] = None
