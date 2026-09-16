from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.expense_splitting.model import ParticipantShare
from src.expense_splitting.service import BalanceCalculationService

router = APIRouter(prefix="/expenses", tags=["expenses"])


class ExpenseParticipantInput(BaseModel):
    user_id: str = Field(..., min_length=1)
    share_amount: float = Field(..., ge=0)


class ExpenseCreateRequest(BaseModel):
    creator: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    total_amount: float = Field(..., gt=0)
    split_type: str = Field(..., pattern="^(equal|custom)$")
    participants: list[ExpenseParticipantInput]


class ExpenseResponse(BaseModel):
    creator: str
    description: str
    total_amount: float
    split_type: str
    participants: list[ExpenseParticipantInput]
    created_at: str


@router.post("/split", response_model=ExpenseResponse)
def create_expense(payload: ExpenseCreateRequest) -> ExpenseResponse:
    service = BalanceCalculationService()
    participants = [ParticipantShare(item.user_id, item.share_amount) for item in payload.participants]
    expense = service.create_expense(
        creator=payload.creator,
        description=payload.description,
        total_amount=payload.total_amount,
        split_type=payload.split_type,
        participants=participants,
    )
    return ExpenseResponse(
        creator=expense.creator,
        description=expense.description,
        total_amount=expense.total_amount,
        split_type=expense.split_type,
        participants=[ExpenseParticipantInput(user_id=item.user_id, share_amount=item.share_amount) for item in expense.participants],
        created_at=expense.created_at.isoformat(),
    )


@router.get("/balances/{user_id}")
def get_balances_for_user(user_id: str) -> dict[str, float]:
    service = BalanceCalculationService()
    participants = [
        ParticipantShare("alice", 50.0),
        ParticipantShare("bob", 50.0),
    ]
    expense = service.create_expense(
        creator="alice",
        description="Dinner",
        total_amount=100.0,
        split_type="equal",
        participants=participants,
    )
    return service.calculate_balances(expense)
