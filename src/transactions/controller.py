from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from src.transactions.service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


class TransactionCreateRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)


class TransactionResponse(BaseModel):
    id: int
    user_id: str
    amount: float
    description: str
    created_at: str


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreateRequest) -> TransactionResponse:
    service = TransactionService()
    transaction = service.create_transaction(
        user_id=payload.user_id,
        amount=payload.amount,
        description=payload.description,
    )
    return TransactionResponse(
        id=transaction.id,
        user_id=transaction.user_id,
        amount=transaction.amount,
        description=transaction.description,
        created_at=transaction.created_at.isoformat(),
    )


@router.get("/{user_id}", response_model=list[TransactionResponse])
def list_transactions_for_user(user_id: str) -> list[TransactionResponse]:
    service = TransactionService()
    transactions = service.get_transactions_for_user(user_id=user_id)
    return [
        TransactionResponse(
            id=transaction.id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            description=transaction.description,
            created_at=transaction.created_at.isoformat(),
        )
        for transaction in transactions
    ]


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_transactions() -> None:
    service = TransactionService()
    service.delete_all_transactions()
