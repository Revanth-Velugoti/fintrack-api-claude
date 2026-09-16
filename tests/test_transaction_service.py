from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database import Base
from src.expense_splitting.model import ParticipantShare
from src.expense_splitting.service import BalanceCalculationService
from src.transactions.repository import TransactionRepository
from src.transactions.service import TransactionService


@pytest.fixture
def transaction_service() -> TransactionService:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    repository = TransactionRepository(session=session)
    return TransactionService(repository=repository)


def test_create_transaction_persists_valid_record(transaction_service: TransactionService) -> None:
    tx = transaction_service.create_transaction("u-1", 25.5, "Groceries")

    assert tx.id is not None
    assert tx.user_id == "u-1"
    assert tx.amount == 25.5
    assert tx.description == "Groceries"


def test_create_transaction_rejects_non_positive_amount(transaction_service: TransactionService) -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        transaction_service.create_transaction("u-2", 0, "Bad amount")


def test_create_transaction_rejects_blank_user_id(transaction_service: TransactionService) -> None:
    with pytest.raises(ValueError, match="user_id is required"):
        transaction_service.create_transaction("   ", 30.0, "Blank user")


def test_get_transactions_for_user_returns_only_that_user(transaction_service: TransactionService) -> None:
    transaction_service.create_transaction("u-1", 10.0, "Coffee")
    transaction_service.create_transaction("u-2", 20.0, "Lunch")

    items = transaction_service.get_transactions_for_user("u-1")

    assert len(items) == 1
    assert items[0].user_id == "u-1"
    assert items[0].description == "Coffee"


def test_delete_all_transactions_removes_all_rows(transaction_service: TransactionService) -> None:
    transaction_service.create_transaction("u-1", 10.0, "A")
    transaction_service.create_transaction("u-2", 20.0, "B")

    deleted = transaction_service.delete_all_transactions()

    assert deleted == 2
    assert transaction_service.get_transactions_for_user("u-1") == []


def test_equal_split_creates_equal_participant_shares() -> None:
    service = BalanceCalculationService()
    expense = service.create_expense(
        creator="alice",
        description="Dinner",
        total_amount=120.0,
        split_type="equal",
        participants=[
            ParticipantShare(user_id="alice", share_amount=0.0),
            ParticipantShare(user_id="bob", share_amount=0.0),
        ],
    )

    assert expense.split_type == "equal"
    assert [participant.share_amount for participant in expense.participants] == [60.0, 60.0]


def test_custom_split_requires_total_match() -> None:
    service = BalanceCalculationService()

    with pytest.raises(ValueError, match="Custom split shares must equal the total amount"):
        service.create_expense(
            creator="alice",
            description="Rent",
            total_amount=100.0,
            split_type="custom",
            participants=[
                ParticipantShare(user_id="alice", share_amount=40.0),
                ParticipantShare(user_id="bob", share_amount=30.0),
            ],
        )


def test_calculate_balances_reports_owed_and_owing() -> None:
    service = BalanceCalculationService()
    expense = service.create_expense(
        creator="alice",
        description="Dinner",
        total_amount=100.0,
        split_type="equal",
        participants=[
            ParticipantShare(user_id="alice", share_amount=0.0),
            ParticipantShare(user_id="bob", share_amount=0.0),
        ],
    )

    balances = service.calculate_balances(expense)

    assert balances["alice"] == 50.0
    assert balances["bob"] == -50.0
