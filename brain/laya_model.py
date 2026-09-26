from laya import Router

class LayaRouter:
    def __init__(self):
        self.router = Router(prefix="/api/v1/laya", tags=["Laya"],preload=True,)

laya_router = LayaRouter()