from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.transactions.model import Transaction


class TransactionRepository:
    def __init__(self, session: Session | None = None) -> None:
        self.session = session or SessionLocal()

    def add(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def list_by_user(self, user_id: str) -> list[Transaction]:
        return self.session.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.created_at.desc()).all()

    def list_all(self) -> list[Transaction]:
        return self.session.query(Transaction).order_by(Transaction.created_at.desc()).all()

    def delete_all(self) -> int:
        deleted = self.session.query(Transaction).delete()
        self.session.commit()
        return deleted

    def close(self) -> None:
        self.session.close()
