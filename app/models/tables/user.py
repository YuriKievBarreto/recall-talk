from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import StrEnum

class ProficiencyLevel(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"
    


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    name: str = Field(min_length=1, max_length=100)
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
    )

    native_language: str = Field(default="pt-BR", max_length=10)
    target_language: str = Field(default="en", max_length=10)
    proficiency_level: str = Field(default=ProficiencyLevel.A1, max_length=2)
    password_hash: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    is_active: bool = Field(default=True)

    speaking_sessions: list["SpeakingSession"] = Relationship(
        back_populates="user"
    )

    review_cards: list["ReviewCard"] = Relationship(
        back_populates="user"
    )