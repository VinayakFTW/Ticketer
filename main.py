from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

server = FastAPI(name="Ticketer Server", version="0.1.0")

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
