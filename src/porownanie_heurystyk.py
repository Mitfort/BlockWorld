"""Powtarzalne porównanie dwóch heurystyk IDA* na wspólnych problemach."""
import csv
import random
from math import inf
from pathlib import Path
from statistics import mean

from src.algorytmy import (
    heurystyka_obowiazkowych_ruchow,
    heurystyka_podloza,
    ida_star,
    weryfikuj_sekwencje,
)
from src.generator import generuj_losowy_stan
from src.stan import StanKlockow
from src.warianty import Warianty

ROZMIARY = (6, 8, 10, 12, 15)
LICZBA_PROBLEMOW = 5
LIMIT_WEZLOW = 30000
ZIARNO_BAZOWE = 20261019


def porownaj_heurystyki(
    *,
    katalog_wynikow: Path | None = None,
    rozmiary: tuple[int, ...] = ROZMIARY,
    liczba_problemow: int = LICZBA_PROBLEMOW,
    warianty: tuple[Warianty, ...] = (Warianty.ROZSZERZONY,),
    limit_wezlow: int = LIMIT_WEZLOW,
    ziarno: int = ZIARNO_BAZOWE,
) -> list[dict]:
    """
    Porównuje działanie algorytmu IDA* z obiema heurystykami (h1 i h2)
    na losowych problemach dla zadanych rozmiarów N i zapisuje wyniki do CSV.
    """
    if katalog_wynikow is None:
        katalog_wynikow = Path(__file__).parent.parent / "wyniki"
    katalog_wynikow.mkdir(parents=True, exist_ok=True)

    wyniki: list[dict] = []

    for wariant in warianty:
        print(f"\n=== PORÓWNANIE HEURYSTYK IDA* (Wariant: {wariant.name}) ===")
        print(f"Limit węzłów: {limit_wezlow}, Ziarno bazowe: {ziarno}\n")

        for n in rozmiary:
            print(f"--- Rozmiar N = {n} ---")
            wezly_h1_lista, czas_h1_lista = [], []
            wezly_h2_lista, czas_h2_lista = [], []
            wspolne_wezly_h1, wspolne_czas_h1 = [], []
            wspolne_wezly_h2, wspolne_czas_h2 = [], []
            sukcesy_h1, sukcesy_h2 = 0, 0
            zgodne_dlugosci = 0
            wspolne_sukcesy = 0

            for numer in range(1, liczba_problemow + 1):
                ziarno_problemu = ziarno + 100 * n + numer
                rng = random.Random(ziarno_problemu)

                start = generuj_losowy_stan(n, wariant, rng=rng)
                cel = generuj_losowy_stan(n, wariant, rng=rng)
                while start.podloza == cel.podloza:
                    cel = generuj_losowy_stan(n, wariant, rng=rng)

                # Heurystyka 1: liczba błędnych podłoży
                sek_h1, wezly_h1, czas_h1, suk_h1, pam_h1 = ida_star(
                    StanKlockow(list(start.podloza), wariant),
                    StanKlockow(list(cel.podloza), wariant),
                    limit_wezlow=limit_wezlow,
                    limit_czasu=inf,
                    heurystyka=heurystyka_podloza,
                )

                # Heurystyka 2: obowiązkowe ruchy
                sek_h2, wezly_h2, czas_h2, suk_h2, pam_h2 = ida_star(
                    StanKlockow(list(start.podloza), wariant),
                    StanKlockow(list(cel.podloza), wariant),
                    limit_wezlow=limit_wezlow,
                    limit_czasu=inf,
                    heurystyka=heurystyka_obowiazkowych_ruchow,
                )

                dl_h1 = len(sek_h1) if suk_h1 and sek_h1 is not None else None
                dl_h2 = len(sek_h2) if suk_h2 and sek_h2 is not None else None

                if suk_h1:
                    ok1, msg1 = weryfikuj_sekwencje(start, cel, sek_h1)
                    assert ok1, f"Błąd weryfikacji h1: {msg1}"
                    sukcesy_h1 += 1

                if suk_h2:
                    ok2, msg2 = weryfikuj_sekwencje(start, cel, sek_h2)
                    assert ok2, f"Błąd weryfikacji h2: {msg2}"
                    sukcesy_h2 += 1

                wezly_h1_lista.append(wezly_h1)
                czas_h1_lista.append(czas_h1)
                wezly_h2_lista.append(wezly_h2)
                czas_h2_lista.append(czas_h2)

                rowne_dlugosci = None
                if suk_h1 and suk_h2:
                    wspolne_sukcesy += 1
                    wspolne_wezly_h1.append(wezly_h1)
                    wspolne_czas_h1.append(czas_h1)
                    wspolne_wezly_h2.append(wezly_h2)
                    wspolne_czas_h2.append(czas_h2)
                    rowne_dlugosci = dl_h1 == dl_h2
                    if rowne_dlugosci:
                        zgodne_dlugosci += 1

                print(
                    f"  Problem {numer} (seed={ziarno_problemu}): "
                    f"h1 -> [sukces={suk_h1}, dł={dl_h1}, węzły={wezly_h1}, czas={czas_h1:.4f}s] | "
                    f"h2 -> [sukces={suk_h2}, dł={dl_h2}, węzły={wezly_h2}, czas={czas_h2:.4f}s] | "
                    f"Równe dł.: {rowne_dlugosci}"
                )

                wiersz = {
                    "wariant": wariant.name,
                    "N": n,
                    "problem": numer,
                    "ziarno": ziarno_problemu,
                    "start": list(start.podloza),
                    "cel": list(cel.podloza),
                    "h1_sukces": suk_h1,
                    "h1_dlugosc": dl_h1,
                    "h1_wezly": wezly_h1,
                    "h1_czas_s": round(czas_h1, 5),
                    "h2_sukces": suk_h2,
                    "h2_dlugosc": dl_h2,
                    "h2_wezly": wezly_h2,
                    "h2_czas_s": round(czas_h2, 5),
                    "rowne_dlugosci": rowne_dlugosci,
                }
                wyniki.append(wiersz)

            print(f"  Podsumowanie N={n} ({wariant.name}):")
            print(f"    Rozwiązane problemy: h1 = {sukcesy_h1}/{liczba_problemow}, h2 = {sukcesy_h2}/{liczba_problemow}")
            print(f"    Średnie węzły (wszystkie): h1 = {mean(wezly_h1_lista):.1f}, h2 = {mean(wezly_h2_lista):.1f}")
            print(f"    Średni czas (wszystkie):   h1 = {mean(czas_h1_lista):.4f}s, h2 = {mean(czas_h2_lista):.4f}s")
            if wspolne_sukcesy > 0:
                print(f"    Średnie węzły (wspólne {wspolne_sukcesy}): h1 = {mean(wspolne_wezly_h1):.1f}, h2 = {mean(wspolne_wezly_h2):.1f}")
                print(f"    Średni czas (wspólne {wspolne_sukcesy}):   h1 = {mean(wspolne_czas_h1):.4f}s, h2 = {mean(wspolne_czas_h2):.4f}s")
                print(f"    Zgodność długości sekwencji: {zgodne_dlugosci}/{wspolne_sukcesy}\n")
            else:
                print("    Brak wspólnie rozwiązanych problemów.\n")

    sciezka_csv = katalog_wynikow / "wyniki.csv"
    with sciezka_csv.open("w", encoding="utf-8", newline="") as plik:
        writer = csv.DictWriter(plik, fieldnames=list(wyniki[0].keys()))
        writer.writeheader()
        writer.writerows(wyniki)

    print(f"Zapisano wyniki do pliku: {sciezka_csv}")
    return wyniki


if __name__ == "__main__":
    porownaj_heurystyki(warianty=(Warianty.ROZSZERZONY, Warianty.PODSTAWOWY))