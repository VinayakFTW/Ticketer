from laya import Router
from brain.config import TicketDecision


class LayaRouter:
    def __init__(self):
        self.router = Router(
            preload=True,
            device="cuda",
        )

    def get_router(self):
        return self.router

    def get_decision(self, request):
        result: TicketDecision = self.router.decide(
            state=request,
            schema=TicketDecision,
            model="multilingual",
            max_len=8192,
        )
        return result
