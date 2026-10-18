from app import models
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings


def get_engine():
    engine = create_engine(settings.DATABASE_URL)
    return engine

def create_tables() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)

def drop_tables() -> None:
    engine = get_engine()
    SQLModel.metadata.drop_all(engine)


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
