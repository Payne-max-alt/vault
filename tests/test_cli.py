from datetime import date
from pathlib import Path

from budget_app.cli import app


def run_command(tmp_path: Path, *args: str) -> str:
    data_file = tmp_path / "data.json"
    argv = ["--data-file", str(data_file), *args]
    return app(argv)


def test_add_and_list(tmp_path: Path) -> None:
    run_command(tmp_path, "add-income", "1200", "pensja", "--date", "2023-06-01")
    run_command(tmp_path, "add-expense", "200", "zakupy", "--description", "warzywa")

    output = run_command(tmp_path, "list")

    assert "pensja" in output
    assert "zakupy" in output


def test_summary_and_balance_commands(tmp_path: Path) -> None:
    run_command(tmp_path, "add-income", "3000", "pensja")
    run_command(tmp_path, "add-expense", "1200", "czynsz")

    summary = run_command(tmp_path, "summary")
    balance = run_command(tmp_path, "balance")

    assert "pensja" in summary
    assert "czynsz" in summary
    assert "Aktualny bilans" in balance
