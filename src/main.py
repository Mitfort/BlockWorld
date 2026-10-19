import sys
from pathlib import Path

from src.algorytmy import (
    bfs,
    dfs,
    heurystyka_obowiazkowych_ruchow,
    heurystyka_podloza,
    ida_star,
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

    # 4. Przeszukanie przestrzeni stanów (DFS)
    sekwencja, wezly, czas, sukces, pamiec_dfs = dfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    if sukces and sekwencja is not None:
        print(" SUKCES (DFS) ")
        print(f"  Długość sekwencji: {len(sekwencja)} ruchów")
        print(f"  Rozwinięte węzły: {wezly}")
        print(f"  Maksymalna liczba stanów w pamięci: {pamiec_dfs}")
        print(f"  Czas wykonania:    {czas:.4f} s")
        print(f"  Sekwencja ruchów:  {sekwencja}\n")

        ok_wer, msg_wer = weryfikuj_sekwencje(start, cel, sekwencja)
        print(" WERYFIKACJA SEKWENCJI (DFS) ")
        if ok_wer:
            print(f"  Status: ✓ {msg_wer}")
        else:
            print(f"  Status: X {msg_wer}")
    else:
        print("X Nie udało się znaleźć rozwiązania w podanych limitach (DFS).")

    ### BFS ###
    sekwencja_bfs, wezly_bfs, czas_bfs, sukces_bfs, pamiec_bfs = bfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    if sukces_bfs and sekwencja_bfs is not None:
        print("\n SUKCES (BFS) ")
        print(f"  Długość sekwencji: {len(sekwencja_bfs)} ruchów")
        print(f"  Rozwinięte węzły: {wezly_bfs}")
        print(f"  Maksymalna liczba stanów w pamięci: {pamiec_bfs}")
        print(f"  Czas wykonania:    {czas_bfs:.4f} s")
        print(f"  Sekwencja ruchów:  {sekwencja_bfs}\n")

        ok_wer_bfs, msg_wer_bfs = weryfikuj_sekwencje(start, cel, sekwencja_bfs)
        print(" WERYFIKACJA SEKWENCJI (BFS) ")
        if ok_wer_bfs:
            print(f"  Status: ✓ {msg_wer_bfs}")
        else:
            print(f"  Status: X {msg_wer_bfs}")
    else:
        print("X Nie udało się znaleźć rozwiązania w podanych limitach (BFS).")

    ### IDA* (Heurystyka 1 - błędne podłoża) ###
    sekwencja_ida1, wezly_ida1, czas_ida1, sukces_ida1, pamiec_ida1 = ida_star(
        start, cel, limit_wezlow=50000, limit_czasu=10.0, heurystyka=heurystyka_podloza
    )

    if sukces_ida1 and sekwencja_ida1 is not None:
        print("\n SUKCES (IDA* - Heurystyka 1: podłoża) ")
        print(f"  Długość sekwencji: {len(sekwencja_ida1)} ruchów")
        print(f"  Rozwinięte węzły: {wezly_ida1}")
        print(f"  Maksymalna liczba stanów na ścieżce: {pamiec_ida1}")
        print(f"  Czas wykonania:    {czas_ida1:.4f} s")
        print(f"  Sekwencja ruchów:  {sekwencja_ida1}\n")

        ok_wer_ida1, msg_wer_ida1 = weryfikuj_sekwencje(start, cel, sekwencja_ida1)
        print(" WERYFIKACJA SEKWENCJI (IDA* - h1) ")
        if ok_wer_ida1:
            print(f"  Status: ✓ {msg_wer_ida1}")
        else:
            print(f"  Status: X {msg_wer_ida1}")
    else:
        print("X Nie udało się znaleźć rozwiązania w podanych limitach (IDA* - h1).")

    ### IDA* (Heurystyka 2 - obowiązkowe ruchy) ###
    sekwencja_ida2, wezly_ida2, czas_ida2, sukces_ida2, pamiec_ida2 = ida_star(
        start, cel, limit_wezlow=50000, limit_czasu=10.0, heurystyka=heurystyka_obowiazkowych_ruchow
    )

    if sukces_ida2 and sekwencja_ida2 is not None:
        print("\n SUKCES (IDA* - Heurystyka 2: obowiązkowe ruchy) ")
        print(f"  Długość sekwencji: {len(sekwencja_ida2)} ruchów")
        print(f"  Rozwinięte węzły: {wezly_ida2}")
        print(f"  Maksymalna liczba stanów na ścieżce: {pamiec_ida2}")
        print(f"  Czas wykonania:    {czas_ida2:.4f} s")
        print(f"  Sekwencja ruchów:  {sekwencja_ida2}\n")

        ok_wer_ida2, msg_wer_ida2 = weryfikuj_sekwencje(start, cel, sekwencja_ida2)
        print(" WERYFIKACJA SEKWENCJI (IDA* - h2) ")
        if ok_wer_ida2:
            print(f"  Status: ✓ {msg_wer_ida2}")
        else:
            print(f"  Status: X {msg_wer_ida2}")
    else:
        print("X Nie udało się znaleźć rozwiązania w podanych limitach (IDA* - h2).")


if __name__ == "__main__":
    main()