import sys
from pathlib import Path

from algorytmy import dfs, weryfikuj_sekwencje
from parser import Parser
from stan import StanKlockow


def main():
    if len(sys.argv) > 1:
        sciezka_pliku = Path(sys.argv[1])
    else:
        sciezka_pliku = Path("dane.txt")
    # 1. Parsowanie pliku
    parser = Parser()
    try:
        start_dane, cel_dane = parser.parse(sciezka_pliku)
        print(f"  Układ początkowy: {start_dane}")
        print(f"  Układ docelowy:   {cel_dane}\n")
    except Exception as e:
        print(f"X Błąd podczas odczytu pliku: {e}")
        return

    # 2. Tworzenie obiektów StanKlockow
    start = StanKlockow(start_dane)
    cel = StanKlockow(cel_dane)

    # 3. Walidacja układów wejściowych
    ok_start, msg_start = start.funkcjaWalidacyjna()
    ok_cel, msg_cel = cel.funkcjaWalidacyjna()

    if not ok_start:
        print(f"X Błąd w stanie początkowym: {msg_start}")
        return
    if not ok_cel:
        print(f"X Błąd w stanie docelowym: {msg_cel}")
        return

    print("✓ Układy wejściowe są poprawne.\n")

    # 4. Pr przeszukanie przestrzeni stanów (DFS)
    sekwencja, wezly, czas, sukces = dfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    # 5. Prezentacja wyników i weryfikacja
    if sukces:
        print(f" SUKCES ")
        print(f"  Długość sekwencji: {len(sekwencja)} ruchów")
        print(f"  Rozwinięte węzły: {wezly}")
        print(f"  Czas wykonania:    {czas:.4f} s")
        print(f"  Sekwencja ruchów:  {sekwencja}\n")

        # Procedura weryfikująca
        ok_wer, msg_wer = weryfikuj_sekwencje(start, cel, sekwencja)
        print(f" WERYFIKACJA SEKWENCJI ")
        if ok_wer:
            print(f"  Status: ✓ {msg_wer}")
        else:
            print(f"  Status: X {msg_wer}")
    else:
        print("X Nie udało się znaleźć rozwiązania w podanych limitach.")

if __name__ == "__main__":
    main()