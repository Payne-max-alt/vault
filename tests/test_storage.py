from datetime import date
from pathlib import Path

from budget_app.storage import BudgetStore, Transaction, balance, summarize


def test_transaction_serialization_roundtrip(tmp_path: Path) -> None:
    store = BudgetStore(tmp_path / "data.json")
    transaction = Transaction.create(
        type="income",
        amount=1200.5,
        category="pensja",
        description="wynagrodzenie",
        date_=date(2023, 6, 1),
    )

    store.save([transaction])
    loaded = store.load()

    assert loaded == [transaction]


def test_summary_and_balance(tmp_path: Path) -> None:
    store = BudgetStore(tmp_path / "data.json")
    transactions = [
        Transaction.create(
            type="income",
            amount=2000,
            category="pensja",
            description="",
            date_=date(2023, 6, 1),
        ),
        Transaction.create(
            type="expense",
            amount=500,
            category="mieszkanie",
            description="",
            date_=date(2023, 6, 2),
        ),
        Transaction.create(
            type="expense",
            amount=300,
            category="jedzenie",
            description="",
            date_=date(2023, 6, 3),
        ),
    ]
    store.save(transactions)

    summary = summarize(store.load())

    assert summary["pensja"]["income"] == 2000
    assert summary["mieszkanie"]["expense"] == 500
    assert summary["jedzenie"]["expense"] == 300
    assert balance(transactions) == 1200
