from sqlalchemy import String, Enum, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base


# Таблица Категория
class Category(Base):
    __tablename__ = 'Category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    type: Mapped[str] = mapped_column(Enum('доход', 'расход', name='transactiontype'), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)

    user = relationship('User', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category')


