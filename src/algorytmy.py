#algorytmy.py
import time
from collections.abc import Callable
from math import inf

from src.stan import StanKlockow
from src.warianty import Warianty
def dfs(
        stanStartowy: StanKlockow, stanDocelowy: StanKlockow, limit_wezlow: int = 10000, limit_czasu: float= 1000
) -> tuple[list[tuple[int, int]] | None, int, float, bool, int]:
    czas_start=time.time()

    stos = [(stanStartowy, [])]
    maksymalna_liczba_stanow_w_pamieci: int = 1

    odwiezone=set()

    rozwiniete_wezly = 0
    while stos:
        czas_aktualny = time.time() - czas_start
        aktualna_liczba_stanow_w_pamieci = len(stos)
        maksymalna_liczba_stanow_w_pamieci = max(maksymalna_liczba_stanow_w_pamieci, aktualna_liczba_stanow_w_pamieci)

        if czas_aktualny > limit_czasu:
            print("przekroczono czas oczekiwania")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci
        if rozwiniete_wezly >= limit_wezlow:
            print("Przekroczono limit rozwiniętych węzłów")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci
        stan_aktualny, sciezka = stos.pop()
        klucz = tuple(stan_aktualny.podloza)

        if klucz in odwiezone:
            continue

        odwiezone.add(klucz)
        rozwiniete_wezly +=1

        if stan_aktualny.podloza == stanDocelowy.podloza:
            return sciezka, rozwiniete_wezly, czas_aktualny, True, maksymalna_liczba_stanow_w_pamieci

        ruchy=stan_aktualny.generuj_ruchy()


        for ruch in reversed(ruchy):
            nastepny_stan = stan_aktualny.wykonajRuch(ruch)
            if tuple(nastepny_stan.podloza) not in odwiezone:
                stos.append((nastepny_stan, sciezka + [ruch]))
    czas_aktualny = time.time() - czas_start
    return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci


# BFS =======
def bfs(stanStartowy: StanKlockow, stanDocelowy: StanKlockow, limit_wezlow: int = 10000, limit_czasu: float = 1000) -> tuple[list[tuple[int, int]] | None, int, float, bool, int]:
    """
    Implementacja algorytmu BFS
    Returns: 
        sekwencja_ruchow: list[tuple[int, int]] | None: Sekwencja ruchów prowadząca do rozwiązania lub None, jeśli nie znaleziono rozwiązania.
        rozwiniete_wezly: int: Liczba rozwiniętych węzłów podczas przeszukiwania.
        czas_aktualny: float: Czas wykonania algorytmu w sekundach.
        sukces: bool: True, jeśli znaleziono rozwiązanie, False w przeciwnym razie.
        maksymalna_liczba_stanow_w_pamieci: int: Maksymalna liczba stanów przechowywanych w pamięci podczas przeszukiwania.
    """

    from collections import deque 

    czas_start = time.time()

    q = deque([(stanStartowy, [])])
    visited = set()
    rozwiniete_wezly = 0
    maksymalna_liczba_stanow_w_pamieci: int = 1

    while q: 

        czas_aktualny = time.time() - czas_start
        aktualna_liczba_stanow_w_pamieci = len(q)

        maksymalna_liczba_stanow_w_pamieci = max(maksymalna_liczba_stanow_w_pamieci, aktualna_liczba_stanow_w_pamieci)

        if czas_aktualny > limit_czasu:
            print("przekroczono czas oczekiwania")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci

        if rozwiniete_wezly >= limit_wezlow:
            print("Przekroczono limit rozwiniętych węzłów")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci

        # Pobieramy pierwszy element z kolejki
        stan_aktualny, sciezka = q.popleft()
        # Tworzymy klucz reprezentujący aktualny stan
        klucz = tuple(stan_aktualny.podloza)

        if klucz in visited:
            continue

        visited.add(klucz)  
        rozwiniete_wezly += 1

        # Sprawdzamy, czy osiągnęliśmy stan docelowy
        if stan_aktualny.podloza == stanDocelowy.podloza:
            return sciezka, rozwiniete_wezly, czas_aktualny, True, maksymalna_liczba_stanow_w_pamieci


        # Generujemy możliwe ruchy z aktualnego stanu
        ruchy = stan_aktualny.generuj_ruchy()

        for ruch in ruchy: # Dla każdego możliwego ruchu generujemy następny stan i dodajemy go do kolejki
            nastepny_stan = stan_aktualny.wykonajRuch(ruch)
            if tuple(nastepny_stan.podloza) not in visited:
                q.append((nastepny_stan, sciezka + [ruch]))

    # Nie znaleźliśmy rozwiązania 
    czas_aktualny = time.time() - czas_start
    return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci

#=====


# algorytmy.py
import time
from collections import deque
from collections.abc import Callable
from math import inf

from src.stan import StanKlockow
from src.warianty import Warianty


def dfs(
    stanStartowy: StanKlockow,
    stanDocelowy: StanKlockow,
    limit_wezlow: int = 10000,
    limit_czasu: float = 1000,
) -> tuple[list[tuple[int, int]] | None, int, float, bool, int]:
    czas_start = time.time()

    stos = [(stanStartowy, [])]
    maksymalna_liczba_stanow_w_pamieci: int = 1

    odwiezone = set()

    rozwiniete_wezly = 0
    while stos:
        czas_aktualny = time.time() - czas_start
        aktualna_liczba_stanow_w_pamieci = len(stos)
        maksymalna_liczba_stanow_w_pamieci = max(
            maksymalna_liczba_stanow_w_pamieci, aktualna_liczba_stanow_w_pamieci
        )

        if czas_aktualny > limit_czasu:
            print("przekroczono czas oczekiwania")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci
        if rozwiniete_wezly >= limit_wezlow:
            print("Przekroczono limit rozwiniętych węzłów")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci

        stan_aktualny, sciezka = stos.pop()
        klucz = tuple(stan_aktualny.podloza)

        if klucz in odwiezone:
            continue

        odwiezone.add(klucz)
        rozwiniete_wezly += 1

        if stan_aktualny.podloza == stanDocelowy.podloza:
            return sciezka, rozwiniete_wezly, czas_aktualny, True, maksymalna_liczba_stanow_w_pamieci

        ruchy = stan_aktualny.generuj_ruchy()

        for ruch in reversed(ruchy):
            nastepny_stan = stan_aktualny.wykonajRuch(ruch)
            if tuple(nastepny_stan.podloza) not in odwiezone:
                stos.append((nastepny_stan, sciezka + [ruch]))

    czas_aktualny = time.time() - czas_start
    return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci


# BFS =======
def bfs(
    stanStartowy: StanKlockow,
    stanDocelowy: StanKlockow,
    limit_wezlow: int = 10000,
    limit_czasu: float = 1000,
) -> tuple[list[tuple[int, int]] | None, int, float, bool, int]:
    """
    Implementacja algorytmu BFS.
    """
    czas_start = time.time()

    q = deque([(stanStartowy, [])])
    visited = set()
    rozwiniete_wezly = 0
    maksymalna_liczba_stanow_w_pamieci: int = 1

    while q:
        czas_aktualny = time.time() - czas_start
        aktualna_liczba_stanow_w_pamieci = len(q)

        maksymalna_liczba_stanow_w_pamieci = max(
            maksymalna_liczba_stanow_w_pamieci, aktualna_liczba_stanow_w_pamieci
        )

        if czas_aktualny > limit_czasu:
            print("przekroczono czas oczekiwania")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci

        if rozwiniete_wezly >= limit_wezlow:
            print("Przekroczono limit rozwiniętych węzłów")
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci

        stan_aktualny, sciezka = q.popleft()
        klucz = tuple(stan_aktualny.podloza)

        if klucz in visited:
            continue

        visited.add(klucz)
        rozwiniete_wezly += 1

        if stan_aktualny.podloza == stanDocelowy.podloza:
            return sciezka, rozwiniete_wezly, czas_aktualny, True, maksymalna_liczba_stanow_w_pamieci

        ruchy = stan_aktualny.generuj_ruchy()

        for ruch in ruchy:
            nastepny_stan = stan_aktualny.wykonajRuch(ruch)
            if tuple(nastepny_stan.podloza) not in visited:
                q.append((nastepny_stan, sciezka + [ruch]))

    czas_aktualny = time.time() - czas_start
    return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci


# IDA* i heurystyki =======
def heurystyka_podloza(stan: StanKlockow, stan_docelowy: StanKlockow) -> int:
    """
    Heurystyka h1: liczy klocki, które leżą na innym podłożu niż w układzie docelowym.
    """
    if len(stan.podloza) != len(stan_docelowy.podloza):
        raise ValueError("Stany muszą mieć tę samą liczbę klocków.")

    licznik = 0
    for obecne, docelowe in zip(stan.podloza, stan_docelowy.podloza):
        if obecne != docelowe:
            licznik += 1
    return licznik


def _czy_klocek_ustalony(klocek: int, stan: StanKlockow, stan_docelowy: StanKlockow) -> bool:
    """
    Sprawdza, czy klocek oraz wszystkie klocki pod nim (aż do stołu)
    leżą już na swoich docelowych podłożach.
    """
    aktualny = klocek
    while aktualny != 0:
        obecne_podloze = stan.podloza[aktualny - 1]
        docelowe_podloze = stan_docelowy.podloza[aktualny - 1]
        if obecne_podloze != docelowe_podloze:
            return False
        aktualny = obecne_podloze
    return True


def heurystyka_obowiazkowych_ruchow(stan: StanKlockow, stan_docelowy: StanKlockow) -> int:
    """
    Heurystyka h2: wyznacza dla każdego klocka minimalną liczbę koniecznych ruchów:
    - 0 ruchów, jeśli klocek jest już ustalony (cała wieża pod nim zgadza się z celem),
    - 2 ruchy, jeśli klocek ma poprawne bezpośrednie podłoże, ale coś pod nim trzeba jeszcze przestawić,
    - 2 ruchy w wariancie podstawowym, gdy leży na klocku i docelowo ma leżeć na innym klocku,
    - 1 ruch w pozostałych przypadkach.
    """
    if len(stan.podloza) != len(stan_docelowy.podloza):
        raise ValueError("Stany muszą mieć tę samą liczbę klocków.")

    n = len(stan.podloza)
    ustalony: dict[int, bool] = {0: True}

    for klocek in range(1, n + 1):
        sciezka = []
        aktualny = klocek
        while aktualny not in ustalony:
            sciezka.append(aktualny)
            obecne = stan.podloza[aktualny - 1]
            docelowe = stan_docelowy.podloza[aktualny - 1]
            if obecne != docelowe:
                ustalony[aktualny] = False
                break
            aktualny = obecne

        wynik = ustalony[aktualny]
        for elem in sciezka:
            ustalony[elem] = wynik

    koszt = 0
    for klocek in range(1, n + 1):
        if ustalony[klocek]:
            continue

        obecne = stan.podloza[klocek - 1]
        docelowe = stan_docelowy.podloza[klocek - 1]

        if obecne == docelowe:
            koszt += 2
        elif stan.wariant == Warianty.PODSTAWOWY and obecne != 0 and docelowe != 0:
            koszt += 2
        else:
            koszt += 1

    return koszt


def ida_star(
    stanStartowy: StanKlockow,
    stanDocelowy: StanKlockow,
    limit_wezlow: int = 10000,
    limit_czasu: float = 1000,
    *,
    heurystyka: Callable[[StanKlockow, StanKlockow], int] = heurystyka_podloza,
) -> tuple[list[tuple[int, int]] | None, int, float, bool, int]:
    """
    Implementacja algorytmu Iterative Deepening A* (IDA*).
    """
    czas_start = time.perf_counter()
    prog = heurystyka(stanStartowy, stanDocelowy)

    sciezka: list[tuple[int, int]] = []
    stany_na_sciezce = {tuple(stanStartowy.podloza)}
    rozwiniete_wezly = 0
    maksymalna_liczba_stanow_w_pamieci = 1
    przerwano = False

    def przeszukaj(stan: StanKlockow, g: int, obecny_prog: int | float) -> tuple[bool, int | float]:
        nonlocal rozwiniete_wezly, maksymalna_liczba_stanow_w_pamieci, przerwano

        if time.perf_counter() - czas_start > limit_czasu:
            przerwano = True
            return False, inf

        f = g + heurystyka(stan, stanDocelowy)
        if f > obecny_prog:
            return False, f

        if rozwiniete_wezly >= limit_wezlow:
            przerwano = True
            return False, inf

        rozwiniete_wezly += 1

        if stan.podloza == stanDocelowy.podloza:
            return True, f

        min_przekroczenie = inf
        for ruch in stan.generuj_ruchy():
            nastepny_stan = stan.wykonajRuch(ruch)
            klucz = tuple(nastepny_stan.podloza)

            if klucz in stany_na_sciezce:
                continue

            sciezka.append(ruch)
            stany_na_sciezce.add(klucz)
            maksymalna_liczba_stanow_w_pamieci = max(
                maksymalna_liczba_stanow_w_pamieci, len(stany_na_sciezce)
            )

            sukces, przekroczenie = przeszukaj(nastepny_stan, g + 1, obecny_prog)
            if sukces:
                return True, przekroczenie

            sciezka.pop()
            stany_na_sciezce.remove(klucz)

            if przerwano:
                return False, inf

            if przekroczenie < min_przekroczenie:
                min_przekroczenie = przekroczenie

        return False, min_przekroczenie

    while True:
        sukces, nastepny_prog = przeszukaj(stanStartowy, 0, prog)
        czas_aktualny = time.perf_counter() - czas_start

        if sukces:
            return sciezka, rozwiniete_wezly, czas_aktualny, True, maksymalna_liczba_stanow_w_pamieci
        if przerwano or nastepny_prog == inf:
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci

        prog = nastepny_prog


# Weryfikacja =======
def weryfikuj_sekwencje(
    stan_startowy: StanKlockow,
    stan_docelowy: StanKlockow,
    sekwencja_ruchow: list[tuple[int, int]] | None,
) -> tuple[bool, str]:
    if sekwencja_ruchow is None:
        return False, "Brak sekwencji ruchów do weryfikacji!"

    aktualny_stan = StanKlockow(list(stan_startowy.podloza), stan_startowy.wariant)

    for v, ruch in enumerate(sekwencja_ruchow, start=1):
        klocek, cel = ruch

        if not (1 <= klocek <= aktualny_stan.N):
            return False, f"Ruch nr {v} {ruch}: Klocek {klocek} nie istnieje!"

        if not (0 <= cel <= aktualny_stan.N):
            return False, f"Ruch nr {v} {ruch}: Docelowe podłoże {cel} nie istnieje!"

        if cel == klocek:
            return (
                False,
                f"Ruch nr {v} {ruch}: Proba polozenia klocka na samym sobie!",
            )

        wolne = aktualny_stan.wolneKlocki()

        if klocek not in wolne:
            return False, f"Ruch nr {v} {ruch}: Klocek {klocek} nie jest wolny!"

        if cel != 0 and cel not in wolne:
            return False, f"Ruch nr {v} {ruch}: Klocek {cel} nie jest wolny!"

        obecne_podloze = aktualny_stan.podloza[klocek - 1]
        if (
            aktualny_stan.wariant == Warianty.PODSTAWOWY
            and obecne_podloze != 0
            and cel != 0
        ):
            return (
                False,
                f"Ruch nr {v} {ruch}: W wariancie podstawowym nie wolno przenosić klocka bezpośrednio z klocka na klocek!",
            )

        aktualny_stan = aktualny_stan.wykonajRuch(ruch)

    if aktualny_stan.podloza == stan_docelowy.podloza:
        return True, f"Sekwencja poprawna ({len(sekwencja_ruchow)} ruchów)"
    else:
        return (
            False,
            f"Sekwencja zakończona, ale układ końcowy {aktualny_stan.podloza} różni się od docelowego {stan_docelowy.podloza}!",
        )