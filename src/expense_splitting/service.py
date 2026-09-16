from __future__ import annotations

from collections.abc import Iterable

from src.expense_splitting.model import ParticipantShare, SharedExpense


class BalanceCalculationService:
    VALID_SPLIT_TYPES = {"equal", "custom"}

    def create_expense(
        self,
        creator: str,
        description: str,
        total_amount: float,
        split_type: str,
        participants: Iterable[ParticipantShare | dict[str, float | str]],
    ) -> SharedExpense:
        cleaned_creator = creator.strip()
        cleaned_description = description.strip()

        if not cleaned_creator:
            raise ValueError("Creator is required.")
        if not cleaned_description:
            raise ValueError("Description is required.")
        if total_amount <= 0:
            raise ValueError("Total amount must be positive.")
        if split_type not in self.VALID_SPLIT_TYPES:
            raise ValueError("Split type must be 'equal' or 'custom'.")

        normalized = self._normalize_participants(participants)
        if not normalized:
            raise ValueError("At least one participant is required.")

        participant_ids = {participant.user_id for participant in normalized}
        if cleaned_creator not in participant_ids:
            normalized.append(ParticipantShare(user_id=cleaned_creator, share_amount=0.0))

        if split_type == "equal":
            equal_share = round(float(total_amount) / len(normalized), 2)
            normalized = [
                ParticipantShare(user_id=participant.user_id, share_amount=equal_share)
                for participant in normalized
            ]
        else:
            self._validate_custom_amounts(total_amount, normalized)

        return SharedExpense(
            creator=cleaned_creator,
            description=cleaned_description,
            total_amount=round(float(total_amount), 2),
            split_type=split_type,
            participants=normalized,
        )

    def calculate_balances(self, expense: SharedExpense) -> dict[str, float]:
        participant_map = {item.user_id: item.share_amount for item in expense.participants}
        if expense.creator not in participant_map:
            raise ValueError("Creator must exist in the participant list.")

        balances: dict[str, float] = {}
        for user_id, share_amount in participant_map.items():
            if user_id == expense.creator:
                balances[user_id] = round(expense.total_amount - share_amount, 2)
            else:
                balances[user_id] = round(-share_amount, 2)
        return balances

    def summarize_pending_balances(self, balances: dict[str, float]) -> dict[str, dict[str, float | list[str]]]:
        summary: dict[str, dict[str, float | list[str]]] = {}
        for user_id, net_amount in balances.items():
            summary[user_id] = {
                "net": round(float(net_amount), 2),
                "owes": [],
                "owed_by": [],
            }
        return summary

    def _normalize_participants(
        self,
        participants: Iterable[ParticipantShare | dict[str, float | str]],
    ) -> list[ParticipantShare]:
        normalized: list[ParticipantShare] = []
        for participant in participants:
            if isinstance(participant, ParticipantShare):
                user_id = participant.user_id.strip()
                share_amount = participant.share_amount
            elif isinstance(participant, dict):
                user_id = str(participant.get("user_id", "")).strip()
                share_amount = float(participant.get("share_amount", 0))
            else:
                raise ValueError("Participant must be a ParticipantShare or a dict.")

            if not user_id:
                raise ValueError("Participant user_id is required.")
            if share_amount < 0:
                raise ValueError(f"Share amount for {user_id} cannot be negative.")
            normalized.append(
                ParticipantShare(
                    user_id=user_id,
                    share_amount=round(float(share_amount), 2),
                )
            )
        return normalized

    def _validate_custom_amounts(self, total_amount: float, participants: list[ParticipantShare]) -> None:
        total_shares = round(sum(item.share_amount for item in participants), 2)
        if total_shares != round(float(total_amount), 2):
            raise ValueError("Custom split shares must equal the total amount.")
