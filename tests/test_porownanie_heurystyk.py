"""Testy zapisu porównań i wspólnych danych wejściowych."""
import csv
from src.porownanie_heurystyk import porownaj_heurystyki
from src.warianty import Warianty


def test_porownanie_wspolne_problemy_i_odtwarzalnosc(tmp_path):
    pierwszy = tmp_path / "pierwszy"
    drugi = tmp_path / "drugi"

    wyniki = porownaj_heurystyki(
        katalog_wynikow=pierwszy,
        rozmiary=(3,),
        liczba_problemow=2,
        warianty=(Warianty.PODSTAWOWY, Warianty.ROZSZERZONY),
    )
    powtorzone = porownaj_heurystyki(
        katalog_wynikow=drugi,
        rozmiary=(3,),
        liczba_problemow=2,
        warianty=(Warianty.PODSTAWOWY, Warianty.ROZSZERZONY),
    )

    with (pierwszy / "wyniki.csv").open(encoding="utf-8", newline="") as plik:
        wiersze = list(csv.DictReader(plik))

    assert len(wyniki) == len(wiersze) == 4
    assert all(w["rowne_dlugosci"] is True for w in wyniki)

    for a, b in zip(wyniki, powtorzone):
        assert a["start"] == b["start"]
        assert a["cel"] == b["cel"]
        assert a["ziarno"] == b["ziarno"]
        assert a["h1_wezly"] == b["h1_wezly"]
        assert a["h2_wezly"] == b["h2_wezly"]
        assert a["h1_dlugosc"] == b["h1_dlugosc"]
        assert a["h2_dlugosc"] == b["h2_dlugosc"]


def test_limit_nie_oznacza_rownych_dlugosci(tmp_path):
    wyniki = porownaj_heurystyki(
        katalog_wynikow=tmp_path / "limit",
        rozmiary=(4,),
        liczba_problemow=1,
        warianty=(Warianty.PODSTAWOWY,),
        limit_wezlow=1,
    )

    assert wyniki[0]["h1_sukces"] is False
    assert wyniki[0]["h2_sukces"] is False
    assert wyniki[0]["rowne_dlugosci"] is None