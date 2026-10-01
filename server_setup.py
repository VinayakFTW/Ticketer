from schemas.postgredb_schema import Base, Engine
from schemas.postgredb_schema import User, Ticket

Base.metadata.create_all(Engine)
