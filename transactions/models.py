from sqlalchemy import Numeric, Enum, TIMESTAMP, func, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base
from datetime import datetime



# Таблица Транзакция
class Transaction(Base):
    __tablename__ = 'Transaction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    type: Mapped[str] = mapped_column(Enum('доход', 'расход', name='transactiontype'), nullable=False)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('Category.id', ondelete="SET NULL"))

    user = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')
