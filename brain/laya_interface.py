import asyncio
import os
import torch
from laya import Router

from brain.config import TicketDecision


class LayaRouter:
    def __init__(self):
        configured_device = os.getenv("DEVICE")
        device = (
            configured_device
            if configured_device
            else ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.router = Router(
            preload=False,
            device=device,
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
