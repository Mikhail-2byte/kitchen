from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv


DB_HOST = "localhost"
DB_PORT = 5432
DB_USERS = "postres"
DB_PASS = "postres"
DB_NAME = "postres"
load_dotenv()

DATABASE_URL = f"pstgresql+asyncpg://{DB_USERS}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
