from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ParticipantShare:
    user_id: str
    share_amount: float


@dataclass
class SharedExpense:
    creator: str
    description: str
    total_amount: float
    split_type: str
    participants: list[ParticipantShare]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
