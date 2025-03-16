from sqlalchemy.future import select
from src.transactions.models import Transaction
from src.database import AsyncSession


# CRUD операции для Транзакции

async def create_transaction(user_id: int, amount: float, transaction_type: str, category_id: int = None,
                             description: str = None) -> Transaction:
    async with AsyncSession() as session:
        new_transaction = Transaction(
            user_id=user_id,
            amount=amount,
            type=transaction_type,
            category_id=category_id,
            description=description
        )
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
        return new_transaction


async def get_transaction_by_id(transaction_id: int) -> Transaction | None:
    async with AsyncSession() as session:
        result = await session.execute(select(Transaction).filter(Transaction.id == transaction_id))
        return result.scalars().first()


async def get_transactions_by_user(user_id: int) -> list[Transaction]:
    async with AsyncSession() as session:
        result = await session.execute(select(Transaction).filter(Transaction.user_id == user_id))
        return result.scalars().all()


async def update_transaction(
        transaction_id: int, amount: float = None, transaction_type: str = None, category_id: int = None,
        description: str = None
) -> Transaction | None:
    async with AsyncSession() as session:
        result = await session.execute(select(Transaction).filter(Transaction.id == transaction_id))
        transaction_to_update = result.scalars().first()
        if transaction_to_update:
            if amount is not None:
                transaction_to_update.amount = amount
            if transaction_type:
                transaction_to_update.type = transaction_type
            if category_id is not None:
                transaction_to_update.category_id = category_id
            if description:
                transaction_to_update.description = description
            await session.commit()
        return transaction_to_update


async def delete_transaction(transaction_id: int) -> bool:
    async with AsyncSession() as session:
        result = await session.execute(select(Transaction).filter(Transaction.id == transaction_id))
        transaction_to_delete = result.scalars().first()
        if transaction_to_delete:
            await session.delete(transaction_to_delete)
            await session.commit()
            return True
        return False
