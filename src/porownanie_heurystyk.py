"""Powtarzalne porównanie dwóch heurystyk IDA* na wspólnych problemach."""

import argparse
import csv
import json
import platform
import random
from dataclasses import asdict, dataclass
from datetime import datetime
from math import inf
from pathlib import Path
from statistics import mean

from src.algorytmy import (
    heurystyka_obowiazkowych_ruchow,
    heurystyka_podloza,
    ida_star,
)
from src.generator import generuj_losowy_stan
from src.stan import StanKlockow
from src.warianty import Warianty

HEURYSTYKI = {
    "h1_podloza": heurystyka_podloza,
    "h2_obowiazkowe_ruchy": heurystyka_obowiazkowych_ruchow,
}


@dataclass(frozen=True)
class WynikHeurystyki:
    h_start: int
    sukces: bool
    wezly: int
    czas_s: float
    dlugosc: int | None
    sekwencja: list[tuple[int, int]] | None
    maks_stanow_na_sciezce: int
    status: str


@dataclass(frozen=True)
class WynikProblemu:
    n: int
    problem: int
    ziarno: int
    wariant: str
    start: list[int]
    cel: list[int]
    wyniki: dict[str, WynikHeurystyki]
    rowne_dlugosci: bool | None


def porownaj_heurystyki(
    *,
    katalog_wynikow: Path,
    rozmiary: tuple[int, ...] = (6, 8, 10, 12, 15),
    liczba_problemow: int = 5,
    warianty: tuple[Warianty, ...] = tuple(Warianty),
    limit_wezlow: int = 30000,
    ziarno: int = 20261019,
) -> list[WynikProblemu]:
    """Uruchamia heurystyki sekwencyjnie i zapisuje dane oraz raport HTML.

    Limit czasu jest wyłączony, żeby o przerwaniu decydował limit rozwinięć.
    Każda para układów jest wspólna dla obu heurystyk i obu wariantów.
    Kolejność heurystyk zmienia się między problemami. Rozkład losowania
    jest rozkładem istniejącego generatora wież, nie jednostajnym po stanach.

    Raises:
        ValueError: Gdy konfiguracja zawiera niedodatnie rozmiary lub limity.
        FileExistsError: Gdy katalog wynikowy już istnieje.
        RuntimeError: Gdy algorytm zwróci nielegalną sekwencję.
    """
    if not rozmiary or min(rozmiary) < 2 or liczba_problemow < 1 or limit_wezlow < 1 or not warianty:
        raise ValueError("Wymagane N >= 2, liczba_problemow >= 1, limit_wezlow >= 1 i co najmniej jeden wariant.")
    katalog_wynikow.mkdir(parents=True, exist_ok=False)
    konfiguracja = {
        "rozmiary": rozmiary,
        "problemow_na_n": liczba_problemow,
        "warianty": [wariant.name for wariant in warianty],
        "limit_wezlow": limit_wezlow,
        "limit_czasu": None,
        "ziarno_bazowe": ziarno,
        "wzor_ziarna": "ziarno_bazowe + 100 * N + numer_problemu (od 1)",
        "python": platform.python_version(),
        "system": platform.platform(),
        "czas_rozpoczecia": datetime.now().astimezone().isoformat(),
        "definicja_wezlow": "Suma odwiedzin w progu f we wszystkich iteracjach, łącznie z celem.",
        "pomiar_czasu": "perf_counter wewnątrz ida_star; bez generowania, weryfikacji i zapisu.",
        "powtorzenia_pomiaru": 1,
    }
    wyniki: list[WynikProblemu] = []

    # Krótka rozgrzewka poza pomiarami właściwych problemów.
    for heurystyka in HEURYSTYKI.values():
        ida_star(StanKlockow([0, 1, 0]), StanKlockow([0, 3, 0]), heurystyka=heurystyka)

    with (katalog_wynikow / "przebieg.jsonl").open("w", encoding="utf-8") as dziennik:
        for n in rozmiary:
            for numer in range(1, liczba_problemow + 1):
                ziarno_problemu = ziarno + 100 * n + numer
                rng = random.Random(ziarno_problemu)
                start = generuj_losowy_stan(n, rng=rng)
                cel = generuj_losowy_stan(n, rng=rng)
                while start.podloza == cel.podloza:
                    cel = generuj_losowy_stan(n, rng=rng)

                for wariant in warianty:
                    stan_startowy = StanKlockow(start.podloza.copy(), wariant)
                    stan_docelowy = StanKlockow(cel.podloza.copy(), wariant)
                    kolejnosc = list(HEURYSTYKI)
                    if (numer + wariant.value) % 2:
                        kolejnosc.reverse()
                    para = {}
                    for nazwa in kolejnosc:
                        heurystyka = HEURYSTYKI[nazwa]
                        sekwencja, wezly, czas, sukces, pamiec = ida_star(
                            stan_startowy,
                            stan_docelowy,
                            limit_wezlow=limit_wezlow,
                            limit_czasu=inf,
                            heurystyka=heurystyka,
                        )
                        if sukces:
                            _sprawdz_sekwencje(stan_startowy, stan_docelowy, sekwencja)
                        para[nazwa] = WynikHeurystyki(
                            h_start=heurystyka(stan_startowy, stan_docelowy),
                            sukces=sukces,
                            wezly=wezly,
                            czas_s=czas,
                            dlugosc=len(sekwencja) if sekwencja is not None else None,
                            sekwencja=sekwencja,
                            maks_stanow_na_sciezce=pamiec,
                            status="OK" if sukces else "LIMIT_WEZLOW" if wezly >= limit_wezlow else "BRAK_ROZWIAZANIA",
                        )
                        print(
                            f"N={n:2} P={numer} {wariant.name:11} {nazwa:22} "
                            f"{para[nazwa].status:12} węzły={wezly:6} czas={czas:.4f}s "
                            f"długość={para[nazwa].dlugosc}",
                            flush=True,
                        )
                    h1, h2 = (para[nazwa] for nazwa in HEURYSTYKI)
                    wynik = WynikProblemu(
                        n=n,
                        problem=numer,
                        ziarno=ziarno_problemu,
                        wariant=wariant.name,
                        start=start.podloza.copy(),
                        cel=cel.podloza.copy(),
                        wyniki={nazwa: para[nazwa] for nazwa in HEURYSTYKI},
                        rowne_dlugosci=h1.dlugosc == h2.dlugosc if h1.sukces and h2.sukces else None,
                    )
                    wyniki.append(wynik)
                    dziennik.write(json.dumps(asdict(wynik), ensure_ascii=False) + "\n")
                    dziennik.flush()

    dane = {
        "konfiguracja": konfiguracja,
        "podsumowanie": podsumuj_wyniki(wyniki),
        "problemy": [asdict(wynik) for wynik in wyniki],
    }
    dane_json = json.dumps(dane, ensure_ascii=False, indent=2)
    (katalog_wynikow / "wyniki.json").write_text(dane_json + "\n", encoding="utf-8")
    _zapisz_csv(katalog_wynikow / "wyniki.csv", wyniki)
    szablon = Path(__file__).with_name("raport_heurystyk.html").read_text(encoding="utf-8")
    (katalog_wynikow / "raport.html").write_text(
        szablon.replace("__DANE_POROWNANIA__", dane_json.replace("</", "<\\/")), encoding="utf-8"
    )
    return wyniki


def _sprawdz_sekwencje(
    start: StanKlockow, cel: StanKlockow, sekwencja: list[tuple[int, int]] | None
) -> None:
    """Weryfikuje każdy ruch według badanego wariantu i sprawdza stan końcowy."""
    if sekwencja is None:
        raise RuntimeError("Sukces bez sekwencji ruchów.")
    aktualny = start
    for ruch in sekwencja:
        if ruch not in aktualny.generuj_ruchy():
            raise RuntimeError(f"Nielegalny ruch {ruch} w wariancie {start.wariant.name}.")
        aktualny = aktualny.wykonajRuch(ruch)
    if aktualny.podloza != cel.podloza:
        raise RuntimeError("Sekwencja nie prowadzi do celu.")


def podsumuj_wyniki(wyniki: list[WynikProblemu]) -> list[dict]:
    """Zwraca średnie po wszystkich próbach i osobno po wspólnie rozwiązanych."""
    podsumowanie = []
    grupy = sorted({(wynik.wariant, wynik.n) for wynik in wyniki})
    for wariant, n in grupy:
        grupa = [wynik for wynik in wyniki if (wynik.wariant, wynik.n) == (wariant, n)]
        wspolne = [wynik for wynik in grupa if wynik.rowne_dlugosci is not None]
        metryki = {}
        for nazwa in HEURYSTYKI:
            proby = [wynik.wyniki[nazwa] for wynik in grupa]
            porownywalne = [wynik.wyniki[nazwa] for wynik in wspolne]
            metryki[nazwa] = {
                "sukcesy": sum(proba.sukces for proba in proby),
                "srednie_wezly_wszystkie": mean(proba.wezly for proba in proby),
                "sredni_czas_s_wszystkie": mean(proba.czas_s for proba in proby),
                "srednie_wezly_wspolne": mean(p.wezly for p in porownywalne) if porownywalne else None,
                "sredni_czas_s_wspolne": mean(p.czas_s for p in porownywalne) if porownywalne else None,
            }
        podsumowanie.append({
            "wariant": wariant,
            "n": n,
            "liczba_problemow": len(grupa),
            "wspolnie_rozwiazane": len(wspolne),
            "rowne_dlugosci": sum(wynik.rowne_dlugosci is True for wynik in grupa),
            "rozne_dlugosci": sum(wynik.rowne_dlugosci is False for wynik in grupa),
            "metryki": metryki,
        })
    return podsumowanie


def _zapisz_csv(sciezka: Path, wyniki: list[WynikProblemu]) -> None:
    """Zapisuje jedną porównywalną parę wyników na wiersz."""
    wiersze = []
    for wynik in wyniki:
        wiersz = {
            "N": wynik.n,
            "problem": wynik.problem,
            "ziarno": wynik.ziarno,
            "wariant": wynik.wariant,
            "start": json.dumps(wynik.start),
            "cel": json.dumps(wynik.cel),
        }
        for skrot, nazwa in zip(("h1", "h2"), HEURYSTYKI, strict=True):
            proba = wynik.wyniki[nazwa]
            for pole in ("h_start", "status", "wezly", "czas_s", "dlugosc"):
                wiersz[f"{skrot}_{pole}"] = getattr(proba, pole)
        wiersz["rowne_dlugosci"] = (
            "TAK" if wynik.rowne_dlugosci is True else "NIE" if wynik.rowne_dlugosci is False else "NIEPOROWNYWALNE"
        )
        wiersze.append(wiersz)
    with sciezka.open("w", encoding="utf-8-sig", newline="") as plik:
        writer = csv.DictWriter(plik, fieldnames=list(wiersze[0]))
        writer.writeheader()
        writer.writerows(wiersze)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit-wezlow", type=int, default=30000)
    parser.add_argument("--ziarno", type=int, default=20261019)
    parser.add_argument("--wariant", choices=("1", "2", "oba"), default="oba")
    parser.add_argument("--rozmiary", type=int, nargs="+", default=[6, 8, 10, 12, 15])
    parser.add_argument("--problemow", type=int, default=5)
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).parent.parent / "wyniki" / "heurystyki_ida_star",
    )
    args = parser.parse_args()
    warianty = tuple(Warianty) if args.wariant == "oba" else (Warianty(int(args.wariant)),)
    porownaj_heurystyki(
        katalog_wynikow=args.output_dir,
        rozmiary=tuple(args.rozmiary),
        liczba_problemow=args.problemow,
        warianty=warianty,
        limit_wezlow=args.limit_wezlow,
        ziarno=args.ziarno,
    )
    print(f"Raport: {args.output_dir.resolve() / 'raport.html'}")


if __name__ == "__main__":
    main()
