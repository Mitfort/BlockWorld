# experiments.py
import random
from src.algorytmy import dfs, weryfikuj_sekwencje,bfs
from src.generator import generuj_losowy_stan
from src.warianty import Warianty
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "wyniki"

def przeprowadz_badania():
    ZIARNO = 42
    random.seed(ZIARNO)

    LIMIT_WEZLOW = 30000
    LIMIT_CZASU = 3.0

    for N in range(3, 16):
        print(f"\n--- TESTY DLA N = {N} ---")

        for i in range(1, 6):  # 5 problemów dla każdego N
            start = generuj_losowy_stan(N)
            cel = generuj_losowy_stan(N)

            while start.podloza == cel.podloza:
                cel = generuj_losowy_stan(N)

            sekwencja, wezly, czas, sukces, _ = dfs(
                start, cel, limit_wezlow=LIMIT_WEZLOW, limit_czasu=LIMIT_CZASU
            )

            if sukces and sekwencja is not None:
                ok, msg = weryfikuj_sekwencje(start, cel, sekwencja)
                status_wer = "TAK" if ok else f"BŁĄD: {msg}"
                dlugosc = len(sekwencja)
            else:
                status_wer = "N/A (Przekroczono limit)"
                dlugosc = "N/A"

            print(f"\nProblem {i} (N={N}):")
            print(f"  Start:    {start.podloza}")
            print(f"  Cel:      {cel.podloza}")
            print(f"  Długość:  {dlugosc}")
            print(f"  Węzły:    {wezly}")
            print(f"  Czas:     {czas:.4f} s")
            print(f"  Weryf.:   {status_wer}")

            if sukces and N < 8:
                print(f"  Ruchy:    {sekwencja}")

def porownaj_algorytmy(wariant: Warianty, ziarna:list[int], N:int):
    """
    Porównuje algorytmy DFS i BFS
    Args:
        wariant (Warianty): Wariant algorytmu do porównania.
        ziarno (int): Ziarno dla generatora losowego.
        N (int): Liczba klocków w problemie.
    """
    
    Limit_wezlow = 30000
    Limit_czasu = 10.0 

    for ziarno in ziarna:
        random.seed(ziarno)
        start = generuj_losowy_stan(N)
        cel = generuj_losowy_stan(N)

        seq_dfs, wezly_dfs, czas_dfs, sukces_dfs, maksymalna_liczba_stanow_w_pamieci_dfs = dfs(
            start, cel, limit_wezlow=Limit_wezlow, limit_czasu=Limit_czasu
        )

        seq_bfs, wezly_bfs, czas_bfs, sukces_bfs, maksymalna_liczba_stanow_w_pamieci_bfs = bfs(
            start, cel, limit_wezlow=Limit_wezlow, limit_czasu=Limit_czasu
        )

        print(f"\nZiarno: {ziarno}, N: {N}")
        print(f"== DFS ==")
        if sukces_dfs and seq_dfs is not None:
            print(f"  Sukces: TAK")
            print(f"  Długość sekwencji: {len(seq_dfs)}")
            print(f"  Rozwinięte węzły: {wezly_dfs}")
            print(f"  Czas wykonania: {czas_dfs:.4f} s")
            print(f"  Maksymalna liczba stanów w pamięci: {maksymalna_liczba_stanow_w_pamieci_dfs}")
        else:
            print(f"  Sukces: NIE (Przekroczono limit)")

        print(f"\n== BFS ==")
        if sukces_bfs and seq_bfs is not None:
            print(f"  Sukces: TAK")
            print(f"  Długość sekwencji: {len(seq_bfs)}")
            print(f"  Rozwinięte węzły: {wezly_bfs}")
            print(f"  Czas wykonania: {czas_bfs:.4f} s")
            print(f"  Maksymalna liczba stanów w pamięci: {maksymalna_liczba_stanow_w_pamieci_bfs}")
        else:
            print(f"  Sukces: NIE (Przekroczono limit)")


if __name__ == "__main__":
    #przeprowadz_badania()
    porownaj_algorytmy(Warianty.ROZSZERZONY, [1,2,3,4,5,6,7,8,9,10], 8)