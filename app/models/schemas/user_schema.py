from sqlmodel import SQLModel
from app.models.tables.user import ProficiencyLevel

class UserCreate(SQLModel):
    name: str 
    email: str 

    native_language: str 
    target_language: str 
    proficiency_level: ProficiencyLevel
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    native_language: str | None = None
    target_language: str | None = None
    proficiency_level: ProficiencyLevel | None = None
    password: str | None = None
    is_active: bool | None = None