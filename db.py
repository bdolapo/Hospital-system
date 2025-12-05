from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

import models  # after Base is created

DATABASE_URL = "sqlite:///./data/hospital.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


