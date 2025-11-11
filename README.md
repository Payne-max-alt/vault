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

Uruchom aplikację poleceniem (bez kopiowania znaków \`\`\` z początku i końca bloku):

```bash
python main.py <polecenie>
```

### Przykłady poleceń

Poniższe przykłady możesz skopiować wprost do terminala (np. PowerShell na Windowsie
lub dowolnej powłoce na Linuksie/macOS):

```bash
# dodanie przychodu
python main.py add-income 3500 pensja --description "Wynagrodzenie" --date 2024-10-05

# dodanie wydatku
python main.py add-expense 120 jedzenie --description "Zakupy spożywcze"

# lista wszystkich transakcji
python main.py list

# podsumowanie kategorii
python main.py summary

# aktualny bilans
python main.py balance
```

Polecenia przyjmują następujące argumenty:

- `add-income <kwota> <kategoria> [--description OPIS] [--date RRRR-MM-DD]` - dodaje przychód.
- `add-expense <kwota> <kategoria> [--description OPIS] [--date RRRR-MM-DD]` - dodaje wydatek.
- `list` - wyświetla wszystkie transakcje.
- `summary` - pokazuje podsumowanie według kategorii.
- `balance` - wyświetla bilans.

Domyślnie dane zapisywane są w pliku `~/.budget/transactions.json` (np. na Windowsie:
`C:\Users\TwojeImie\.budget\transactions.json`). Możesz zmienić lokalizację pliku
dodając argument `--data-file PATH` do dowolnego polecenia, np. `python main.py list --data-file budzet.json`.

## Testy

```bash
pytest
```
