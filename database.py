# backend/db.py
from sqlmodel import SQLModel, create_engine, Session
import os

DB_FILE = os.getenv("HOSPITAL_DB", "hospital.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

# NOTE: check_same_thread False is OK for SQLite single process (Streamlit).
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
