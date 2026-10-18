import sys
from pathlib import Path

from src.algorytmy import (
    dfs, 
    bfs,
    weryfikuj_sekwencje,
)

from src.parser import Parser
from src.stan import StanKlockow
from src.warianty import Warianty

HOME_PATH = Path(__file__).parent.parent
WARIANT = Warianty.ROZSZERZONY

def main():
    if len(sys.argv) > 1:
        sciezka_pliku = HOME_PATH / "data" / sys.argv[1]
        wariant_value = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        wariant = Warianty(wariant_value)
    else:
        sciezka_pliku = HOME_PATH / "data" / "test_sample.txt"
        wariant = WARIANT

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
    start = StanKlockow(start_dane, wariant)
    cel = StanKlockow(cel_dane, wariant)

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
    sekwencja, wezly, czas, sukces, _ = dfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    # 5. Prezentacja wyników i weryfikacja
    if sukces and sekwencja is not None:
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


    ### BFS ### 

    sekwencja_bfs, wezly_bfs, czas_bfs, sukces_bfs, _ = bfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    if sukces_bfs and sekwencja_bfs is not None:
        print(f"\n SUKCES (BFS) ")
        print(f"  Długość sekwencji: {len(sekwencja_bfs)} ruchów")
        print(f"  Rozwinięte węzły: {wezly_bfs}")
        print(f"  Czas wykonania:    {czas_bfs:.4f} s")
        print(f"  Sekwencja ruchów:  {sekwencja_bfs}\n")

        # Procedura weryfikująca
        ok_wer_bfs, msg_wer_bfs = weryfikuj_sekwencje(start, cel, sekwencja_bfs)
        print(f" WERYFIKACJA SEKWENCJI (BFS) ")
        if ok_wer_bfs:
            print(f"  Status: ✓ {msg_wer_bfs}")
        else:
            print(f"  Status: X {msg_wer_bfs}")
    else:
        print("X Nie udało się znaleźć rozwiązania w podanych limitach (BFS).")


if __name__ == "__main__":
    main()