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
    average_results = {
        "DFS": {"success": 0, "total_time": 0.0, "total_nodes": 0, "total_memory": 0, "solutions": 0},
        "BFS": {"success": 0, "total_time": 0.0, "total_nodes": 0, "total_memory": 0, "solutions": 0}
    }

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
            average_results["DFS"]["success"] += 1
            average_results["DFS"]["total_time"] += czas_dfs
            average_results["DFS"]["total_nodes"] += wezly_dfs
            average_results["DFS"]["total_memory"] += maksymalna_liczba_stanow_w_pamieci_dfs
            average_results["DFS"]["solutions"] += len(seq_dfs)

            print(f"  Sukces: TAK")
            print(f"  Długość sekwencji: {len(seq_dfs)}")
            print(f"  Rozwinięte węzły: {wezly_dfs}")
            print(f"  Czas wykonania: {czas_dfs:.4f} s")
            print(f"  Maksymalna liczba stanów w pamięci: {maksymalna_liczba_stanow_w_pamieci_dfs}")
        else:
            print(f"  Sukces: NIE (Przekroczono limit)")

        print(f"\n== BFS ==")
        if sukces_bfs and seq_bfs is not None:
            average_results["BFS"]["success"] += 1
            average_results["BFS"]["total_time"] += czas_bfs
            average_results["BFS"]["total_nodes"] += wezly_bfs
            average_results["BFS"]["total_memory"] += maksymalna_liczba_stanow_w_pamieci_bfs
            average_results["BFS"]["solutions"] += len(seq_bfs)
        
            print(f"  Sukces: TAK")
            print(f"  Długość sekwencji: {len(seq_bfs)}")
            print(f"  Rozwinięte węzły: {wezly_bfs}")
            print(f"  Czas wykonania: {czas_bfs:.4f} s")
            print(f"  Maksymalna liczba stanów w pamięci: {maksymalna_liczba_stanow_w_pamieci_bfs}")
        else:
            print(f"  Sukces: NIE (Przekroczono limit)")

    print(f"\n=== Średnie wyniki ===")
    for algorytm in average_results:
        if average_results[algorytm]["success"] > 0:
            print(f"\n{algorytm}:")
            print(f"  Średni czas: {average_results[algorytm]['total_time'] / average_results[algorytm]['success']:.4f} s")
            print(f"  Średnia liczba węzłów: {average_results[algorytm]['total_nodes'] / average_results[algorytm]['success']}")
            print(f"  Średnia liczba stanów w pamięci: {average_results[algorytm]['total_memory'] / average_results[algorytm]['success']}")
            print(f"  Średnia długość sekwencji: {average_results[algorytm]['solutions'] / average_results[algorytm]['success']}")
        else:
            print(f"\n{algorytm}: Brak sukcesów (przekroczono limity)")

    output_file = RESULTS_DIR / f"porownanie_algorytmow_N{N}.txt"

    with open(output_file, "w") as f:
        f.write(f"Porównanie algorytmów DFS i BFS dla N={N}\n")
        f.write(f"Ziarna: {ziarna}\n")
        f.write(f"Limit węzłów: {Limit_wezlow}, Limit czasu: {Limit_czasu} s\n\n")

        for algorytm in average_results:
            if average_results[algorytm]["success"] > 0:
                f.write(f"{algorytm}:\n")
                f.write(f"  Średni czas: {average_results[algorytm]['total_time'] / average_results[algorytm]['success']:.4f} s\n")
                f.write(f"  Średnia liczba węzłów: {average_results[algorytm]['total_nodes'] / average_results[algorytm]['success']}\n")
                f.write(f"  Średnia liczba stanów w pamięci: {average_results[algorytm]['total_memory'] / average_results[algorytm]['success']}\n")
                f.write(f"  Średnia długość sekwencji: {average_results[algorytm]['solutions'] / average_results[algorytm]['success']}\n\n")
            else:
                f.write(f"{algorytm}: Brak sukcesów (przekroczono limity)\n\n")


if __name__ == "__main__":
    #przeprowadz_badania()
    porownaj_algorytmy(Warianty.ROZSZERZONY, [1,2,3,4,5,6,7,8,9,10], 8)