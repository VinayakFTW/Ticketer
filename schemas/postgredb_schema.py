from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum, UUID, create_engine
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from typing import Optional, List
from datetime import datetime
import uuid

from brain.config import ENVIRONMENT_VARIABLES
from schemas.enums import TicketPriority, TicketStatus, UserRole

Engine = create_engine(ENVIRONMENT_VARIABLES.get("POSTGRES_URL"), echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    institute: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    role: Mapped[Optional[UserRole]] = mapped_column(
        Enum(UserRole), default=UserRole.STUDENT, nullable=False
    )
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    priority: Mapped[Optional[TicketPriority]] = mapped_column(
        Enum(TicketPriority), nullable=True
    )
    is_safety_grievance: Mapped[Optional[bool]] = mapped_column(nullable=True)
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False
    )
    assigned_email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bump_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_bump_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="tickets")


class Sessions(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    messages: Mapped[str] = mapped_column(String, nullable=False)  # JSON string
