import os
from typing import Literal
from pydantic import BaseModel, Field


SYSTEM_PROMPT = """
You are a helpful assistant that provides information about the Ticketer system.
You should only provide factual information about the system and avoid making up information.

"""

ENVIRONMENT_VARIABLES = {
    "OPENAI_BASE_URL": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    "POSTGRES_URL": os.environ.get("POSTGRES_URL", ""),
}


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
