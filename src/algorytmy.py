#algorytmy.py
import time
from src.stan import StanKlockow
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
