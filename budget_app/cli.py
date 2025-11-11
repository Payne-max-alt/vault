"""Command line interface for the budget management application."""
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, List

from .storage import BudgetStore, Transaction, summarize, balance


def parse_date(value: str) -> date:
    """Parse a date string in ISO format."""

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:  # pragma: no cover - defensive programming
        raise argparse.ArgumentTypeError(str(exc)) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Domowe zarządzanie budżetem")
    parser.add_argument(
        "--data-file",
        type=Path,
        default=Path.home() / ".budget" / "transactions.json",
        help="Ścieżka do pliku z danymi (domyślnie ~/.budget/transactions.json).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_common = argparse.ArgumentParser(add_help=False)
    add_common.add_argument("amount", type=float, help="Kwota transakcji")
    add_common.add_argument("category", help="Kategoria (np. jedzenie, mieszkanie)")
    add_common.add_argument(
        "--description",
        default="",
        help="Opcjonalny opis transakcji",
    )
    add_common.add_argument(
        "--date",
        type=parse_date,
        default=date.today(),
        help="Data transakcji w formacie RRRR-MM-DD (domyślnie dziś)",
    )

    subparsers.add_parser(
        "add-income",
        parents=[add_common],
        help="Dodaj przychód",
    )
    subparsers.add_parser(
        "add-expense",
        parents=[add_common],
        help="Dodaj wydatek",
    )

    subparsers.add_parser("list", help="Wyświetl wszystkie transakcje")
    subparsers.add_parser("summary", help="Podsumowanie kategorii")
    subparsers.add_parser("balance", help="Aktualny bilans budżetu")

    return parser


def ensure_store(path: Path) -> BudgetStore:
    return BudgetStore(path)


def handle_add(
    *,
    store: BudgetStore,
    type_: str,
    amount: float,
    category: str,
    description: str,
    date_: date,
) -> Transaction:
    transactions = store.load()
    transaction = Transaction.create(
        type=type_, amount=amount, category=category, description=description, date_=date_
    )
    transactions.append(transaction)
    store.save(transactions)
    return transaction


def handle_list(transactions: Iterable[Transaction]) -> str:
    if not transactions:
        return "Brak zapisanych transakcji."

    lines = [
        "ID                                 | Data       | Typ     | Kwota    | Kategoria        | Opis",
        "-" * 100,
    ]
    for txn in transactions:
        lines.append(
            f"{txn.id[:32]:<33}| {txn.date.isoformat()} | {txn.type:<7} | "
            f"{txn.amount:>8.2f} | {txn.category:<15} | {txn.description}"
        )
    return "\n".join(lines)


def handle_summary(transactions: Iterable[Transaction]) -> str:
    data = summarize(transactions)
    if not data:
        return "Brak danych do podsumowania."

    lines = [
        "Kategoria          | Przychody | Wydatki | Bilans",
        "-" * 60,
    ]
    for category, totals in sorted(data.items()):
        lines.append(
            f"{category:<18}| {totals['income']:>9.2f} | {totals['expense']:>7.2f} | {totals['net']:>7.2f}"
        )
    return "\n".join(lines)


def handle_balance(transactions: Iterable[Transaction]) -> str:
    return f"Aktualny bilans: {balance(transactions):.2f}"


def app(argv: List[str] | None = None) -> str:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = ensure_store(args.data_file)

    if args.command == "add-income":
        txn = handle_add(
            store=store,
            type_="income",
            amount=args.amount,
            category=args.category,
            description=args.description,
            date_=args.date,
        )
        return f"Dodano przychód {txn.amount:.2f} ({txn.category})"
    if args.command == "add-expense":
        txn = handle_add(
            store=store,
            type_="expense",
            amount=args.amount,
            category=args.category,
            description=args.description,
            date_=args.date,
        )
        return f"Dodano wydatek {txn.amount:.2f} ({txn.category})"

    transactions = store.load()
    if args.command == "list":
        return handle_list(transactions)
    if args.command == "summary":
        return handle_summary(transactions)
    if args.command == "balance":
        return handle_balance(transactions)

    raise RuntimeError(f"Nieobsługiwane polecenie: {args.command}")


def main() -> None:
    print(app())


if __name__ == "__main__":  # pragma: no cover
    main()
