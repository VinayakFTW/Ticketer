from laya import Router
import asyncio

from brain.config import TicketDecision


class LayaRouter:
    def __init__(self):
        self.router = Router(
            preload=True,
            device="cuda",
        )

    def get_router(self):
        return self.router

    async def get_decision(self, request):
        result: TicketDecision = await asyncio.to_thread(
            self.router.decide,
            state=request,
            schema=TicketDecision,
            model="multilingual",
            max_len=8192,
        )
        return result


LAYA = LayaRouter()
