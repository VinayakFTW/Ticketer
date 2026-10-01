from schemas.postgredb_schema import Base, Engine
from schemas.postgredb_schema import User, Ticket, Sessions

Base.metadata.create_all(Engine)
