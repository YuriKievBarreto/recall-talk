
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel, Relationship
from app.models.tables.user import ProficiencyLevel


class ItemType(StrEnum):
    WORD = "WORD"
    EXPRESSION = "EXPRESSION"
    GRAMMAR = "GRAMMAR"


class LearningItemVisibility(StrEnum):
    PERSONAL = "PERSONAL"
    SHARED = "SHARED"


class LearningItemSource(StrEnum):
    USER_CREATED = "USER_CREATED"
    AGENT_SUGGESTED = "AGENT_SUGGESTED"



class LearningItem(SQLModel, table=True):
    __tablename__ = "learning_items"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    content: str = Field(min_length=1, max_length=200)
    normalized_content: str = Field(max_length=200, index=True)
    meaning: str = Field(min_length=1)
    item_type: ItemType
    target_language: str = Field(default="en", max_length=10)
    native_language: str = Field(default="pt-BR", max_length=10)
    example_sentences: str | None = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )
    proficiency_level: str = Field(default=ProficiencyLevel.A1, max_length=2)

    visibility: LearningItemVisibility
    source: LearningItemSource
    

    created_by_user_id: UUID | None = Field(
        default=None,
        foreign_key="users.id",
        index=True,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    review_cards: list["ReviewCard"] = Relationship(
        back_populates="learning_item"
    )

    practice_attempts: list["PracticeAttempt"] = Relationship(
        back_populates="learning_item"
    )
