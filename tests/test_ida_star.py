"""Testy heurystyki, optymalności IDA* i limitów przeszukiwania."""

from collections import deque
from itertools import product

import pytest

from src.algorytmy import (
    bfs,
    heurystyka_obowiazkowych_ruchow,
    heurystyka_podloza,
    ida_star,
    weryfikuj_sekwencje,
)
from src.stan import StanKlockow
from src.warianty import Warianty


@pytest.mark.parametrize(
    "podloza, cel, oczekiwana",
    [
        ([0, 1, 0], [0, 1, 0], 0),
        ([0, 1, 0], [0, 3, 0], 1),
        ([0, 1, 0], [0, 0, 0], 1),
        ([0, 0, 0], [0, 1, 0], 1),
        ([0, 1, 0, 2, 3], [2, 3, 4, 5, 0], 5),
        ([], [], 0),
    ],
)
def test_heurystyka_podloza(podloza, cel, oczekiwana):
    # Arrange
    start = StanKlockow(podloza)
    docelowy = StanKlockow(cel)

    # Act
    wynik = heurystyka_podloza(start, docelowy)

    # Assert
    assert wynik == oczekiwana


@pytest.mark.parametrize(
    "wariant, podloza, cel, dlugosc",
    [
        (Warianty.PODSTAWOWY, [0, 1, 0], [0, 3, 0], 2),
        (Warianty.ROZSZERZONY, [0, 1, 0], [0, 3, 0], 1),
        (Warianty.PODSTAWOWY, [0, 1, 0, 2, 3], [2, 3, 4, 5, 0], 7),
        (Warianty.ROZSZERZONY, [0, 1, 0, 2, 3], [2, 3, 4, 5, 0], 5),
        # Klocek 3 ma poprawne podłoże, ale trzeba go tymczasowo przenieść.
        (Warianty.PODSTAWOWY, [0, 1, 2], [0, 0, 2], 3),
        (Warianty.ROZSZERZONY, [0, 1, 2], [0, 0, 2], 3),
    ],
)
def test_ida_star_najkrotsza_legalna_sekwencja(wariant, podloza, cel, dlugosc):
    # Arrange
    start = StanKlockow(podloza.copy(), wariant)
    docelowy = StanKlockow(cel.copy(), wariant)

    # Act
    sekwencja, wezly, czas, sukces, pamiec = ida_star(start, docelowy)

    # Assert
    assert sukces is True
    assert sekwencja is not None
    assert len(sekwencja) == dlugosc
    assert weryfikuj_sekwencje(start, docelowy, sekwencja)[0] is True
    aktualny = start
    for ruch in sekwencja:
        assert ruch in aktualny.generuj_ruchy()
        aktualny = aktualny.wykonajRuch(ruch)
    assert aktualny.podloza == cel
    assert start.podloza == podloza
    assert docelowy.podloza == cel
    assert wezly > 0
    assert czas >= 0
    assert pamiec >= len(sekwencja) + 1


@pytest.mark.parametrize("podloza", [[], [0], [0, 1, 0]])
def test_ida_star_start_jest_celem(podloza):
    # Arrange
    start = StanKlockow(podloza.copy())
    cel = StanKlockow(podloza.copy())

    # Act
    sekwencja, wezly, czas, sukces, pamiec = ida_star(start, cel)

    # Assert
    assert sukces is True
    assert sekwencja == []
    assert wezly == 1
    assert czas >= 0
    assert pamiec == 1


@pytest.mark.parametrize("wariant", list(Warianty))
@pytest.mark.parametrize("heurystyka", [heurystyka_podloza, heurystyka_obowiazkowych_ruchow])
def test_ida_star_zgodnosc_z_bfs_dla_wszystkich_par_trzech_klockow(wariant, heurystyka):
    # Arrange
    stany = [StanKlockow(list(podloza), wariant) for podloza in product(range(4), repeat=3)]
    poprawne_stany = [stan for stan in stany if stan.funkcjaWalidacyjna()[0]]

    for start, cel in product(poprawne_stany, repeat=2):
        # Act
        sekwencja_ida, _, _, sukces_ida, _ = ida_star(start, cel, heurystyka=heurystyka)
        sekwencja_bfs, _, _, sukces_bfs, _ = bfs(start, cel)

        # Assert
        assert sukces_ida is True
        assert sukces_bfs is True
        assert sekwencja_ida is not None
        assert sekwencja_bfs is not None
        assert len(sekwencja_ida) == len(sekwencja_bfs), (start.podloza, cel.podloza)
        assert weryfikuj_sekwencje(start, cel, sekwencja_ida)[0] is True


@pytest.mark.parametrize("limit_wezlow", [0, 1, 4])
def test_ida_star_limit_wezlow_obejmuje_wszystkie_iteracje(limit_wezlow):
    # Arrange
    start = StanKlockow([0, 1, 2])
    cel = StanKlockow([0, 0, 2])

    # Act
    sekwencja, wezly, _, sukces, _ = ida_star(start, cel, limit_wezlow=limit_wezlow)

    # Assert
    assert sukces is False
    assert sekwencja is None
    assert wezly == limit_wezlow


def test_ida_star_limit_czasu(monkeypatch):
    # Arrange
    start = StanKlockow([0, 1, 2])
    cel = StanKlockow([0, 0, 2])
    odczyt_czasu = 0.0

    def zegar():
        nonlocal odczyt_czasu
        odczyt_czasu += 1.0
        return odczyt_czasu

    monkeypatch.setattr("src.algorytmy.time.perf_counter", zegar)

    # Act
    sekwencja, _, czas, sukces, _ = ida_star(start, cel, limit_czasu=2.0)

    # Assert
    assert sukces is False
    assert sekwencja is None
    assert czas > 2.0


@pytest.mark.parametrize(
    "algorytm", [heurystyka_podloza, heurystyka_obowiazkowych_ruchow, ida_star]
)
def test_rozne_liczby_klockow(algorytm):
    # Arrange
    start = StanKlockow([0])
    cel = StanKlockow([0, 1])

    # Act / Assert
    with pytest.raises(ValueError):
        algorytm(start, cel)


@pytest.mark.parametrize("wariant", list(Warianty))
@pytest.mark.parametrize(
    "podloza, cel, podstawowy, rozszerzony",
    [
        ([], [], 0, 0),
        ([0, 1, 2], [0, 1, 2], 0, 0),
        ([0, 1, 0], [0, 3, 0], 2, 1),
        ([0, 1, 2], [0, 0, 2], 3, 3),
        ([0, 1, 2, 3], [0, 0, 2, 3], 5, 5),
        ([0, 1, 0, 2, 3], [2, 3, 4, 5, 0], 7, 5),
    ],
)
def test_obowiazkowe_ruchy(wariant, podloza, cel, podstawowy, rozszerzony):
    # Arrange
    start = StanKlockow(podloza, wariant)
    docelowy = StanKlockow(cel, wariant)
    oczekiwana = podstawowy if wariant == Warianty.PODSTAWOWY else rozszerzony

    # Act
    wynik = heurystyka_obowiazkowych_ruchow(start, docelowy)

    # Assert
    assert wynik == oczekiwana


@pytest.mark.parametrize("wariant", list(Warianty))
def test_dopuszczalnosc_i_spojnosc_dla_wszystkich_par_czterech_klockow(wariant):
    # Arrange
    kandydaci = [StanKlockow(list(p), wariant) for p in product(range(5), repeat=4)]
    stany = [stan for stan in kandydaci if stan.funkcjaWalidacyjna()[0]]
    sasiedzi = {
        tuple(stan.podloza): [stan.wykonajRuch(ruch) for ruch in stan.generuj_ruchy()]
        for stan in stany
    }

    for cel in stany:
        # Act: wszystkie ruchy są odwracalne, BFS od celu daje dokładne koszty.
        odleglosci = {tuple(cel.podloza): 0}
        kolejka = deque([tuple(cel.podloza)])
        while kolejka:
            klucz = kolejka.popleft()
            for sasiad in sasiedzi[klucz]:
                nowy_klucz = tuple(sasiad.podloza)
                if nowy_klucz not in odleglosci:
                    odleglosci[nowy_klucz] = odleglosci[klucz] + 1
                    kolejka.append(nowy_klucz)
        wartosci = {
            tuple(stan.podloza): heurystyka_obowiazkowych_ruchow(stan, cel)
            for stan in stany
        }

        # Assert: dominacja h1, dopuszczalność i spójność na każdej krawędzi.
        assert wartosci[tuple(cel.podloza)] == 0
        for stan in stany:
            klucz = tuple(stan.podloza)
            assert heurystyka_podloza(stan, cel) <= wartosci[klucz] <= odleglosci[klucz]
            for sasiad in sasiedzi[klucz]:
                assert wartosci[klucz] <= 1 + wartosci[tuple(sasiad.podloza)]
