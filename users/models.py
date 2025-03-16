from sqlalchemy import String, TIMESTAMP, func, Integer
from datetime import datetime

from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base



# Таблица Пользователь
class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())

    categories = relationship('Category', back_populates='user', cascade="all, delete")
    transactions = relationship('Transaction', back_populates='user',
                                                             cascade="all, delete")

