from typing import Literal
from pydantic import BaseModel, Field


class TicketDecision(BaseModel):
    summary_reason: str = Field(
        description="One short sentence summarizing the student's core issue."
    )
    department: Literal[
        "it_support",
        "facilities",
        "academics_admin",
        "student_services",
        "safety_committee",
    ] = Field(
        description=(
            "Primary department responsible:\n"
            "- it_support: Wi-Fi, LMS, network, logins, lab hardware/software.\n"
            "- facilities: Furniture, electrical, water/plumbing, AC, cleaning, pests.\n"
            "- academics_admin: ID cards, fee payments, scholarships, transcripts.\n"
            "- student_services: Library, buses/transport, general queries.\n"
            "- safety_committee: Ragging, harassment, physical danger, threats."
        )
    )
    priority: Literal["low", "medium", "urgent", "critical"] = Field(
        description="Operational urgency based on impact and deadlines."
    )

    is_safety_grievance: bool = Field(
        description="True ONLY if the ticket mentions ragging, harassment, violence, or direct physical danger."
    )


class CreateTicketRequest(BaseModel):
    ticket_id: str
    user_id: str
    text: str
    created_at: str
