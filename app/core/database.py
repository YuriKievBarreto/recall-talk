from app import models
from sqlmodel import SQLModel, create_engine
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

