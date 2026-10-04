import os
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful assistant that provides information about the Ticketer system.
You should only provide factual information about the system and avoid making up information.
"""

SUMMARY_PROMPT = """You are an automated support ticket summarizer. 
Your sole task is to generate a concise, objective, 1-to-2 sentence summary of the issue described in the ticket.

Strict Guidelines:
1. Do NOT include thinking steps, drafts, bullet points, reasoning, or labels.
2. Maintain a neutral, professional, and factual tone (e.g., "User reports that...").
3. Never repeat the prompt, metadata, or instructions in your output.
"""

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "ticket_summary",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "A concise 1-2 sentence objective summary of the ticket issue.",
                }
            },
            "required": ["summary"],
            "additionalProperties": False,
        },
    },
}

ENVIRONMENT_VARIABLES = {
    "OPENAI_BASE_URL": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
    "POSTGRES_URL": os.environ.get("POSTGRES_URL"),
    "JWT_SECRET_KEY": os.environ.get("JWT_SECRET_KEY"),
    "MODE": os.environ.get("MODE"),
}


class TicketSummary(BaseModel):
    summary: str = Field(
        description="A concise 1-2 sentence objective summary of the ticket issue."
    )


class TicketDecision(BaseModel):
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
        description="if the ticket mentions ragging, harassment, violence, or direct physical danger then True, otherwise False."
    )
