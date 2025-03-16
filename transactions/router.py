from fastapi import APIRouter, HTTPException
from src.transactions.schemas import TransactionCreate, TransactionOut
from src.transactions.service import (
    create_transaction,
    get_transaction_by_id,
    get_transactions_by_user,
    update_transaction,
    delete_transaction
)

router = APIRouter()


@router.post("/transactions", response_model=TransactionOut)
async def create_transaction_endpoint(transaction: TransactionCreate):
    try:
        new_transaction = await create_transaction(
            amount=transaction.amount,
            description=transaction.description,
            transaction_type=transaction.type,
            category_id=transaction.category_id,
            user_id=transaction.user_id
        )
        return new_transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions/{transaction_id}", response_model=TransactionOut)
async def get_transaction_endpoint(transaction_id: int):
    try:
        transaction = await get_transaction_by_id(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail=f"Transaction with id {transaction_id} not found.")
        return transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions/user/{user_id}", response_model=list[TransactionOut])
async def get_user_transactions(user_id: int):
    try:
        transactions = await get_transactions_by_user(user_id)
        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found for the given user.")
        return transactions
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching user's transactions.")


@router.put("/transactions/{transaction_id}", response_model=TransactionOut)
async def update_transaction_endpoint(transaction_id: int, transaction: TransactionCreate):
    try:
        updated_transaction = await update_transaction(
            transaction_id=transaction_id,
            amount=transaction.amount,
            description=transaction.description
        )
        if not updated_transaction:
            raise HTTPException(status_code=404, detail=f"Transaction with id {transaction_id} not found.")
        return updated_transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/transactions/{transaction_id}")
async def delete_transaction_endpoint(transaction_id: int):
    try:
        result = await delete_transaction(transaction_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Transaction with id {transaction_id} not found.")
        return {"detail": "Transaction successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
