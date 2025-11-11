# Aplikacja do zarządzania domowym budżetem

Prosta aplikacja CLI pozwalająca na zapisywanie przychodów i wydatków oraz
sprawdzanie aktualnego bilansu.

## Wymagania

- Python 3.11+
- `pip install -r requirements.txt` (jeśli chcesz zainstalować zależności testowe)

## Instalacja

1. Sklonuj repozytorium i przejdź do katalogu projektu.
2. (Opcjonalnie) utwórz środowisko wirtualne.
3. Zainstaluj wymagane pakiety testowe: `pip install pytest`.

## Użycie

Uruchom aplikację poleceniem:

```bash
python main.py <polecenie>
```

Polecenia:

- `add-income <kwota> <kategoria> [--description OPIS] [--date RRRR-MM-DD]` - dodaje przychód.
- `add-expense <kwota> <kategoria> [--description OPIS] [--date RRRR-MM-DD]` - dodaje wydatek.
- `list` - wyświetla wszystkie transakcje.
- `summary` - pokazuje podsumowanie według kategorii.
- `balance` - wyświetla bilans.

Domyślnie dane zapisywane są w pliku `~/.budget/transactions.json`. Możesz zmienić
lokalizację pliku dodając argument `--data-file PATH` do dowolnego polecenia.

## Testy

```bash
pytest
```
