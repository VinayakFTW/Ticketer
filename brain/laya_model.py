from laya import Router
from brain.config import LAYA_TICKET_CONFIG
from schemas.ticket_schema import TicketDecision

class LayaRouter:
    def __init__(self):
        self.router = Router(
            prefix="/api/v1/laya",
            tags=["Laya"],
            preload=True,
            device="cuda",
        )

    def get_router(self):
        return self.router

    def get_decision(self, request):
        # decison = self.router.predict(
        #     state=request,
        #     questions=LAYA_TICKET_CONFIG,
        #     model="multilingual",
        #     max_len=8192,
        # )
        # department = decison["department"]["choice"]
        # priority = decison["priority"]["score"]
        # is_safety = decison["is_safety_grievance"]["boolean"]
        # return (
        #     department,
        #     priority,
        #     is_safety,
        # )
        result: TicketDecision = self.router.decide(
            state=request,
            schema=TicketDecision,
            model="multilingual",
            max_len=8192,
        )
        return result