from laya import Router
from brain.config import LAYA_TICKET_CONFIG


class LayaRouter:
    def __init__(self):
        self.router = Router(
            prefix="/api/v1/laya",
            tags=["Laya"],
            preload=True,
        )

    def get_router(self):
        return self.router

    def get_decision(self, request):
        decison = self.router.predict(state=request, questions=LAYA_TICKET_CONFIG, model="multilingual", max_len=8192)
        return (
            decison["department"]["choice"],
            decison["urgency"]["score"],
            decison["is_safety_grievance"]["noul"],
            decison["routing"]["model"],
        )
