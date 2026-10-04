from enum import Enum


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"


class TicketStatus(str, Enum):
    OPEN = "open"
    AUTO_REPLIED = "auto_replied"
    IN_PROGRESS = "in_progress"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    STAFF = "STAFF"
    ADMIN = "ADMIN"
