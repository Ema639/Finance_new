from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DATABASE_URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer

engine = create_async_engine(DATABASE_URL)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс
class Base(DeclarativeBase):
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)

