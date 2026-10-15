# generator.py
import random
from src.stan import StanKlockow


def generuj_losowy_stan(N: int) -> StanKlockow:
    klocki = list(range(1, N + 1))
    random.shuffle(klocki)

    miejsca_ciecia = sorted(
        random.sample(range(1, N), random.randint(0, N - 1))
    )

    wieze = []
    poprzedni = 0
    for cut in miejsca_ciecia:
        wieze.append(klocki[poprzedni:cut])
        poprzedni = cut
    wieze.append(klocki[poprzedni:])

    podloza = [0] * N
    for wieza in wieze:
        podloza[wieza[0] - 1] = 0
        for i in range(1, len(wieza)):
            podloza[wieza[i] - 1] = wieza[i - 1]

    return StanKlockow(podloza)