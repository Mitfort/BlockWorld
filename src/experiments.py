# experiments.py
import random
from src.algorytmy import dfs, weryfikuj_sekwencje
from src.generator import generuj_losowy_stan


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

            sekwencja, wezly, czas, sukces = dfs(
                start, cel, limit_wezlow=LIMIT_WEZLOW, limit_czasu=LIMIT_CZASU
            )

            if sukces:
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


if __name__ == "__main__":
    przeprowadz_badania()