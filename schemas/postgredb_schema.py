from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from typing import Optional, List
from sqlalchemy import create_engine
from datetime import datetime

from brain.config import ENVIRONMENT_VARIABLES
from schemas.enums import TicketPriority, TicketStatus

Engine = create_engine(ENVIRONMENT_VARIABLES.get("POSTGRES_URL"), echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    institute: Mapped[Optional[str]] = mapped_column(String, nullable=False)

    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="user")


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    language_checkpoint: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    priority: Mapped[Optional[TicketPriority]] = mapped_column(
        Enum(TicketPriority), nullable=True
    )
    is_safety_grievance: Mapped[Optional[bool]] = mapped_column(nullable=True)
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), default="open", nullable=False
    )
    assigned_email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bump_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_bump_time: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="tickets")


class Sessions(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    last_accessed_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    messages: Mapped[str] = mapped_column(String, nullable=False)  # JSON string


Base.metadata.create_all(Engine)
