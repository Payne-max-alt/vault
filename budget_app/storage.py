"""Storage helpers for the budget management application."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
import json
from pathlib import Path
from typing import Dict, Iterable, List, Literal, Optional
import uuid

TransactionType = Literal["income", "expense"]


@dataclass
class Transaction:
    """Represents a budget transaction."""

    id: str
    type: TransactionType
    amount: float
    category: str
    description: str
    date: date

    @classmethod
    def create(
        cls,
        *,
        type: TransactionType,
        amount: float,
        category: str,
        description: str,
        date_: date,
    ) -> "Transaction":
        """Create a new transaction with a generated identifier."""

        return cls(
            id=str(uuid.uuid4()),
            type=type,
            amount=round(float(amount), 2),
            category=category,
            description=description,
            date=date_,
        )

    def serialize(self) -> Dict[str, object]:
        """Convert the transaction into a JSON serializable dictionary."""

        data = asdict(self)
        data["date"] = self.date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Transaction":
        """Recreate a transaction from a dictionary."""

        return cls(
            id=str(data["id"]),
            type=data["type"],
            amount=float(data["amount"]),
            category=str(data.get("category", "uncategorized")),
            description=str(data.get("description", "")),
            date=date.fromisoformat(str(data["date"])),
        )


class BudgetStore:
    """Utility class for loading and storing transactions."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> List[Transaction]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        transactions = payload.get("transactions", [])
        return [Transaction.from_dict(entry) for entry in transactions]

    def save(self, transactions: Iterable[Transaction]) -> None:
        payload = {"transactions": [txn.serialize() for txn in transactions]}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)


def summarize(transactions: Iterable[Transaction]) -> Dict[str, Dict[str, float]]:
    """Create a summary grouped by category with totals for income and expenses."""

    summary: Dict[str, Dict[str, float]] = {}
    for txn in transactions:
        category_entry = summary.setdefault(
            txn.category,
            {"income": 0.0, "expense": 0.0, "net": 0.0},
        )
        category_entry[txn.type] += txn.amount
        category_entry["net"] = round(category_entry["income"] - category_entry["expense"], 2)
    return summary


def balance(transactions: Iterable[Transaction]) -> float:
    """Compute the global balance for provided transactions."""

    total = 0.0
    for txn in transactions:
        if txn.type == "income":
            total += txn.amount
        else:
            total -= txn.amount
    return round(total, 2)
