from __future__ import annotations

from fastapi import FastAPI

from src.database import init_db
from src.expense_splitting.controller import router as expense_router
from src.transactions.controller import router as transaction_router

app = FastAPI(title="FinTrack API")
app.include_router(transaction_router)
app.include_router(expense_router)

init_db()
