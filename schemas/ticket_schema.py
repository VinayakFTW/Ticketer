from typing import TypedDict, Literal
from pydantic import BaseModel

LAYA_TICKET_SCHEMA = {
    "department": {
        "type": "choice",
        "instructions": "Which department handles this college support or grievance request?",
        "criteria": {
            "it_support": "Wi-Fi, campus network, VPN, LMS access, password reset, lab computer hardware/software.",
            "facilities": "Classroom furniture, projectors, electrical, water/plumbing, AC, hostel cleaning, pests.",
            "academics_admin": "Student ID card, fee payment failure, receipts, scholarships, certificates, transcripts.",
            "student_services": "Library book renewal, transport/bus pass, routine complaints.",
            "safety_committee": "Ragging, harassment, physical danger, critical grievance requiring disciplinary intervention."
        }
    },
    "urgency": {
        "type": "score",
        "instructions": "What is the operational urgency or priority level?",
        "criteria": ["low", "medium", "urgent", "critical"]
    },
    "is_safety_grievance": {
        "type": "noul",
        "instructions": "Does this report involve ragging, harassment, safety risks, or emergency physical hazard?"
    }
}

class TicketState(TypedDict):
    ticket_id: str
    user_id: str
    text: str
    language_checkpoint: str
    department: str
    urgency_level: str
    is_safety_grievance: bool
    status: Literal["open", "routed", "bumped", "escalated", "resolved"]
    assigned_email: str
    bump_count: int
    last_bump_time: str

class CreateTicketRequest(BaseModel):
    ticket_id: str
    user_id: str
    text: str
    created_at: str