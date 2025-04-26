import sqlmodel
from .config import DATABASE_URL
from sqlmodel import SQLModel, Session

if DATABASE_URL == '':
    raise NotImplementedError("DATABASE URL Needs to be set")
engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    print("Create database")
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session