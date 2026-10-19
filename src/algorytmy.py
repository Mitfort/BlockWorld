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


### Iterative deepening A* (IDA*) algorithm

def heurystyka_podloza(stan: StanKlockow, stan_docelowy: StanKlockow) -> int:
    """Zwraca liczbę klocków na innym podłożu niż w stanie docelowym.

    Wartość 0 w podloza oznacza stół i jest porównywana tak samo jak numer
    klocka. Jeden ruch zmienia podłoże jednego klocka, więc heurystyka
    nie zawyża liczby ruchów potrzebnych do osiągnięcia celu.

    Raises:
        ValueError: Gdy stany mają różne liczby klocków.
    """
    return sum(
        podloze != podloze_docelowe
        for podloze, podloze_docelowe in zip(
            stan.podloza, stan_docelowy.podloza, strict=True
        )
    )

def heurystyka_obowiazkowych_ruchow(stan: StanKlockow, stan_docelowy: StanKlockow) -> int:
    """Sumuje dolne ograniczenia liczby ruchów poszczególnych klocków.

    Klocek ustalony ma całą wieżę pod sobą zgodną z celem, aż do stołu.
    Klocek nieustalony na poprawnym bezpośrednim podłożu wymaga co najmniej
    dwóch ruchów: zdjęcia, żeby przestawić coś niżej, i powrotu na podłoże.
    Inny nieustalony klocek wymaga co najmniej jednego ruchu. W wariancie
    podstawowym zmiana podłoża z klocka na klocek wymaga dwóch ruchów.
    Każdy ruch dotyczy jednego klocka, więc te ograniczenia można sumować.
    Stany wejściowe powinny być poprawnymi układami klocków.

    Raises:
        ValueError: Gdy stany mają różne liczby klocków.
    """
    if len(stan.podloza) != len(stan_docelowy.podloza):
        raise ValueError("Stany muszą mieć tę samą liczbę klocków.")

    # Pamiętamy wynik dla każdego klocka, żeby przejść wszystkie łańcuchy
    # podłoży łącznie w O(N). Indeks 0 oznacza zawsze ustalony stół.
    ustalone: list[bool | None] = [True] + [None] * len(stan.podloza)
    for klocek in range(1, len(ustalone)):
        lancuch: list[int] = []
        aktualny = klocek
        while ustalone[aktualny] is None:
            podloze = stan.podloza[aktualny - 1]
            if podloze != stan_docelowy.podloza[aktualny - 1]:
                ustalone[aktualny] = False
                break
            lancuch.append(aktualny)
            aktualny = podloze
        for element in lancuch:
            ustalone[element] = ustalone[aktualny]

    koszt = 0
    for klocek, (podloze, docelowe) in enumerate(
        zip(stan.podloza, stan_docelowy.podloza, strict=True), start=1
    ):
        if ustalone[klocek]:
            continue
        if podloze == docelowe or (
            stan.wariant == Warianty.PODSTAWOWY and podloze != 0 and docelowe != 0
        ):
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
    Znajduje najkrótszą sekwencję ruchów za pomocą IDA*.

    Każdy ruch kosztuje 1. Kolejne przeszukiwania DFS ogranicza próg
    f = liczba wykonanych ruchów + heurystyka(stan, cel).
    Stany wejściowe powinny być poprawnymi układami klocków.
    Gwarancja optymalności wymaga dopuszczalnej heurystyki, równej 0 w celu.
    Domyślnie używana jest heurystyka_podloza.

    Returns:
        Sekwencja ruchów lub None, liczba rozwinięć, czas w sekundach, sukces
        i maksymalna liczba stanów na ścieżce. Rozwinięcia są sumowane po
        wszystkich iteracjach, obejmują cel i pomijają węzły odcięte progiem.
        Limity obejmują całe uruchomienie; limit_czasu=inf wyłącza limit czasu.

    Raises:
        ValueError: Gdy stany mają różne liczby klocków.
    """
    czas_start = time.perf_counter()
    prog = heurystyka(stanStartowy, stanDocelowy)
    sciezka: list[tuple[int, int]] = []
    stany_na_sciezce = {tuple(stanStartowy.podloza)}
    rozwiniete_wezly = 0
    maksymalna_liczba_stanow_w_pamieci = 1
    przerwano = False

    def _przeszukaj(stan: StanKlockow, g: int, prog: int | float) -> tuple[bool, int | float]:
        """Przeszukuje ścieżki w progu i zwraca sukces oraz najmniejsze przekroczenie."""
        nonlocal rozwiniete_wezly, maksymalna_liczba_stanow_w_pamieci, przerwano

        if time.perf_counter() - czas_start > limit_czasu:
            przerwano = True
            return False, inf

        f = g + heurystyka(stan, stanDocelowy)
        if f > prog:
            return False, f

        if rozwiniete_wezly >= limit_wezlow:
            przerwano = True
            return False, inf
        rozwiniete_wezly += 1

        if stan.podloza == stanDocelowy.podloza:
            return True, f

        nastepny_prog = inf
        for ruch in stan.generuj_ruchy():
            nastepny_stan = stan.wykonajRuch(ruch)
            klucz = tuple(nastepny_stan.podloza)
            # Unikamy cykli tylko na bieżącej ścieżce. Stan może być ponownie
            # potrzebny na innej ścieżce albo przy większym progu.
            if klucz in stany_na_sciezce:
                continue

            sciezka.append(ruch)
            stany_na_sciezce.add(klucz)
            maksymalna_liczba_stanow_w_pamieci = max(
                maksymalna_liczba_stanow_w_pamieci, len(stany_na_sciezce)
            )
            sukces, przekroczenie = _przeszukaj(nastepny_stan, g + 1, prog)
            if sukces:
                return True, przekroczenie

            sciezka.pop()
            stany_na_sciezce.remove(klucz)
            if przerwano:
                return False, inf
            nastepny_prog = min(nastepny_prog, przekroczenie)

        return False, nastepny_prog

    while True:
        sukces, nastepny_prog = _przeszukaj(stanStartowy, 0, prog)
        czas_aktualny = time.perf_counter() - czas_start
        if sukces:
            return sciezka, rozwiniete_wezly, czas_aktualny, True, maksymalna_liczba_stanow_w_pamieci
        if przerwano or nastepny_prog == inf:
            return None, rozwiniete_wezly, czas_aktualny, False, maksymalna_liczba_stanow_w_pamieci
        # Najmniejsze f odcięte w tej iteracji wyznacza kolejny próg.
        prog = nastepny_prog

#=====

def weryfikuj_sekwencje(stan_startowy: StanKlockow, stan_docelowy: StanKlockow, sekwencja_ruchow: list[tuple[int, int]] | None,) -> tuple[bool, str]:
    if sekwencja_ruchow is None:
        return False, "Brak sekwencji ruchów do weryfikacji!"
    
    aktualny_stan = StanKlockow(list(stan_startowy.podloza))

    for v, ruch in enumerate(sekwencja_ruchow, start=1):
        klocek, cel = ruch
        wolne = aktualny_stan.wolneKlocki()

        if klocek not in wolne:
            return False, f"Ruch nr {v} {ruch}: Klocek {klocek} nie jest wolny!"

        if cel != 0 and cel not in wolne:
            return False, f"Ruch nr {v} {ruch}: Klocek {cel} nie jest wolny!"

        if cel == klocek:
            return (
                False,
                f"Ruch nr {v} {ruch}: Proba polozenia klocka na samym sobie!",
            )

        aktualny_stan = aktualny_stan.wykonajRuch(ruch)

    if aktualny_stan.podloza == stan_docelowy.podloza:
        return True, f"Sekwencja poprawna ({len(sekwencja_ruchow)} ruchów)"
    else:
        return (
            False,
            f"Sekwencja zakończona, ale układ końcowy {aktualny_stan.podloza} różni się od docelowego {stan_docelowy.podloza}!",
        )
