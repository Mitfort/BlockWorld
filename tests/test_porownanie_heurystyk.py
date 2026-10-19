"""Testy zapisu porównań i wspólnych danych wejściowych."""

import csv
import json

import pytest

from src.porownanie_heurystyk import porownaj_heurystyki
from src.warianty import Warianty


def test_porownanie_wspolne_problemy_i_odtwarzalnosc(tmp_path):
    # Arrange
    pierwszy = tmp_path / "pierwszy"
    drugi = tmp_path / "drugi"

    # Act
    wyniki = porownaj_heurystyki(katalog_wynikow=pierwszy, rozmiary=(3,), liczba_problemow=2)
    powtorzone = porownaj_heurystyki(katalog_wynikow=drugi, rozmiary=(3,), liczba_problemow=2)
    dane = json.loads((pierwszy / "wyniki.json").read_text(encoding="utf-8"))
    with (pierwszy / "wyniki.csv").open(encoding="utf-8-sig", newline="") as plik:
        wiersze = list(csv.DictReader(plik))

    # Assert
    assert len(wyniki) == len(wiersze) == 4
    assert all(wynik.rowne_dlugosci is True for wynik in wyniki)
    for i in range(0, len(wyniki), 2):
        assert wyniki[i].start == wyniki[i + 1].start
        assert wyniki[i].cel == wyniki[i + 1].cel
        assert wyniki[i].wariant != wyniki[i + 1].wariant
    for a, b in zip(wyniki, powtorzone, strict=True):
        assert (a.start, a.cel, a.ziarno) == (b.start, b.cel, b.ziarno)
        for heurystyka in a.wyniki:
            assert a.wyniki[heurystyka].wezly == b.wyniki[heurystyka].wezly
            assert a.wyniki[heurystyka].dlugosc == b.wyniki[heurystyka].dlugosc
    assert dane["konfiguracja"]["limit_czasu"] is None
    assert all(grupa["wspolnie_rozwiazane"] == 2 for grupa in dane["podsumowanie"])
    assert "__DANE_POROWNANIA__" not in (pierwszy / "raport.html").read_text(encoding="utf-8")


def test_limit_nie_oznacza_rownych_dlugosci(tmp_path):
    # Act
    wyniki = porownaj_heurystyki(
        katalog_wynikow=tmp_path / "limit",
        rozmiary=(3,),
        liczba_problemow=1,
        warianty=(Warianty.PODSTAWOWY,),
        limit_wezlow=1,
    )

    # Assert
    assert wyniki[0].rowne_dlugosci is None
    assert all(proba.status == "LIMIT_WEZLOW" for proba in wyniki[0].wyniki.values())


def test_istniejace_wyniki_nie_sa_nadpisywane(tmp_path):
    # Act / Assert
    with pytest.raises(FileExistsError):
        porownaj_heurystyki(katalog_wynikow=tmp_path, rozmiary=(3,), liczba_problemow=1)
