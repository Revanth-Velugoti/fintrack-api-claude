from __future__ import annotations

from src.transactions.model import Transaction
from src.transactions.repository import TransactionRepository


class TransactionService:
    def __init__(self, repository: TransactionRepository | None = None) -> None:
        self.repository = repository or TransactionRepository()

    def create_transaction(self, user_id: str, amount: float, description: str) -> Transaction:
        cleaned_user_id = user_id.strip()
        cleaned_description = description.strip()

        if not cleaned_user_id:
            raise ValueError("user_id is required.")
        if amount <= 0:
            raise ValueError("amount must be greater than zero.")
        if not cleaned_description:
            raise ValueError("description is required.")

        transaction = Transaction(
            user_id=cleaned_user_id,
            amount=float(amount),
            description=cleaned_description,
        )
        return self.repository.add(transaction)

    def get_transactions_for_user(self, user_id: str) -> list[Transaction]:
        cleaned_user_id = user_id.strip()
        if not cleaned_user_id:
            raise ValueError("user_id is required.")
        return self.repository.list_by_user(cleaned_user_id)

    def delete_all_transactions(self) -> int:
        return self.repository.delete_all()
