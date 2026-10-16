from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship

from fsrs import Card, State


class ReviewCard(SQLModel, table=True):
    __tablename__ = "review_cards"
    __table_args__ = (
        # Problema 5: fsrs_card_id deve ser único por usuário, não globalmente
        UniqueConstraint("user_id", "fsrs_card_id", name="uq_review_card_user_fsrs"),
        # Problema 6: um usuário não pode ter dois cartões para o mesmo conteúdo
        UniqueConstraint("user_id", "learning_item_id", name="uq_review_card_user_item"),
    )

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
    )

    learning_item_id: UUID = Field(
        foreign_key="learning_items.id",
        index=True,
    )

    # Identificador do Card do FSRS
    fsrs_card_id: int = Field(index=True)

    # Atributos do FSRS
    state: State
    step: int | None = Field(default=None)
    stability: float | None = Field(default=None)
    difficulty: float | None = Field(default=None)
    due: datetime = Field(index=True)
    last_review: datetime | None = Field(default=None)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    user: "User" = Relationship(
        back_populates="review_cards"
    )

    learning_item: "LearningItem" = Relationship(
        back_populates="review_cards"
    )

    practice_attempts: list["PracticeAttempt"] = Relationship(
        back_populates="review_card"
    )

