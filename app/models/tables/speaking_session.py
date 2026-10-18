from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship


class SpeakingSessionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class SpeakingSession(SQLModel, table=True):
    __tablename__ = "speaking_sessions"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
    )

    status: SpeakingSessionStatus = Field(
        default=SpeakingSessionStatus.ACTIVE,
        index=True,
    )

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    ended_at: datetime | None = Field(default=None)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    user: "User" =  Relationship(
        back_populates="speaking_sessions"
    )

    practice_attempts: list["PracticeAttempt"] = Relationship(
        back_populates="speaking_session"
    )