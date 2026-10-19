"""Eksport wykresu wyników badania IDA* do PNG i SVG."""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def zapisz_wykres(sciezka_danych: Path) -> Path:
    """Rysuje średnie wszystkich prób, z uwzględnieniem przerwań limitem."""
    dane = json.loads(sciezka_danych.read_text(encoding="utf-8"))
    konfiguracja = dane["konfiguracja"]
    warianty = konfiguracja["warianty"]
    rozmiary = konfiguracja["rozmiary"]
    fig, osie = plt.subplots(
        len(warianty), 2, figsize=(12, 3.6 * len(warianty)), squeeze=False, sharey="col"
    )
    serie = [
        ("h1_podloza", "h1: błędne podłoża", "#2868a2"),
        ("h2_obowiazkowe_ruchy", "h2: obowiązkowe ruchy", "#a45a12"),
    ]
    for indeks, wariant in enumerate(warianty):
        grupy_wariantu = {g["n"]: g for g in dane["podsumowanie"] if g["wariant"] == wariant}
        grupy = [grupy_wariantu[n] for n in rozmiary]
        nazwa = "Podstawowy" if wariant == "PODSTAWOWY" else "Rozszerzony"
        for kolumna, (pole, etykieta) in enumerate([
            ("srednie_wezly_wszystkie", "Śr. rozwinięcia [węzły]"),
            ("sredni_czas_s_wszystkie", "Śr. czas [s]"),
        ]):
            os = osie[indeks, kolumna]
            for numer, (klucz, legenda, kolor) in enumerate(serie):
                os.bar(
                    [i + (numer - 0.5) * 0.36 for i in range(len(rozmiary))],
                    [g["metryki"][klucz][pole] for g in grupy],
                    width=0.34, color=kolor, label=legenda,
                )
            os.set_title(f"{nazwa} · {'rozwinięcia' if kolumna == 0 else 'czas'}", loc="left")
            os.set_xticks(range(len(rozmiary)), rozmiary)
            os.set_xlabel("Liczba klocków N")
            os.set_ylabel(etykieta)
            os.set_yscale("log")
            os.grid(axis="y", alpha=0.2)
            os.set_axisbelow(True)
            os.spines[["top", "right"]].set_visible(False)
            os.legend(fontsize=8, frameon=False)
    fig.suptitle("Porównanie heurystyk IDA* na tych samych losowych problemach", fontsize=15)
    fig.text(
        0.06, 0.02,
        f"Źródło: {sciezka_danych.name} · {konfiguracja['problemow_na_n']} problemów/N · "
        f"limit {konfiguracja['limit_wezlow']:,} rozwinięć/przebieg.\n"
        "Osie Y: skala logarytmiczna. Średnie obejmują próby przerwane limitem; "
        "ich czas nie jest czasem rozwiązania. Jeden pomiar/przebieg.",
        fontsize=8, color="#536471",
    )
    fig.tight_layout(rect=(0, 0.08, 1, 0.95))
    wyjscie = sciezka_danych.with_name("porownanie.png")
    fig.savefig(wyjscie, dpi=180)
    fig.savefig(wyjscie.with_suffix(".svg"))
    plt.close(fig)
    return wyjscie


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dane", type=Path, help="Ścieżka do wyniki.json")
    args = parser.parse_args()
    print(zapisz_wykres(args.dane))


if __name__ == "__main__":
    main()
