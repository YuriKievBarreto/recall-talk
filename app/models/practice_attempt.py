from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship


class PracticeMode(StrEnum):
    TARGETED = "TARGETED"
    FREE_CONVERSATION = "FREE_CONVERSATION"


class PracticeAttempt(SQLModel, table=True):
    __tablename__ = "practice_attempts"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    speaking_session_id: UUID = Field(
        foreign_key="speaking_sessions.id",
        index=True,
    )

    learning_item_id: UUID | None = Field(
        default=None,
        foreign_key="learning_items.id",
        index=True,
    )

    review_card_id: UUID | None = Field(
        default=None,
        foreign_key="review_cards.id",
        index=True,
    )

    mode: PracticeMode

    # Interação
    prompt: str = Field(min_length=1)
    user_response: str = Field(min_length=1)

    # Avaliação do agente
    feedback: str | None = Field(default=None)
    correction: str | None = Field(default=None)
    score: float | None = Field(default=None, ge=0.0, le=1.0)

    was_successful: bool | None = Field(default=None)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True,
    )

    speaking_session: "SpeakingSession" = Relationship(
        back_populates="practice_attempts"
    )

    learning_item: "LearningItem" = Relationship(
        back_populates="practice_attempts"
    )

    review_card: "ReviewCard" = Relationship(
        back_populates="practice_attempts"
    )