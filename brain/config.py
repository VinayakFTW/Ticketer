SYSTEM_PROMPT = """
You are a helpful assistant that provides information about the Ticketer system.
You should only provide factual information about the system and avoid making up information.

"""

LAYA_TICKET_CONFIG = {
    "department": {
        "type": "choice",
        "instructions": "Which department handles this college support or grievance request?",
        "criteria": {
            "it_support": "Wi-Fi, campus network, VPN, LMS access, password reset, lab computer hardware/software.",
            "facilities": "Classroom furniture, projectors, electrical, water/plumbing, AC, hostel cleaning, pests.",
            "academics_admin": "Student ID card, fee payment failure, receipts, scholarships, certificates, transcripts.",
            "student_services": "Library book renewal, transport/bus pass, routine complaints.",
            "safety_committee": "Ragging, harassment, physical danger, critical grievance requiring disciplinary intervention.",
        },
    },
    "priority": {
        "type": "score",
        "instructions": "Determine operational urgency based on impact and deadlines.",
        "criteria": ["low", "medium", "urgent", "critical"],
    },
    "is_safety_grievance": {
        "type": "boolean",
        "instructions": "Does this report involve ragging, harassment, safety risks, or emergency physical hazard?",
    },
}
