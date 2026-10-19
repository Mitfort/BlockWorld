# generator.py
import random
from src.stan import StanKlockow
from src.warianty import Warianty


def generuj_losowy_stan(
    N: int, wariant: Warianty = Warianty.PODSTAWOWY, *, rng: random.Random | None = None
) -> StanKlockow:
    """Generuje poprawny, losowy stan dla N klocków."""
    klocki = list(range(1, N + 1))

    generator = rng if rng is not None else random
    generator.shuffle(klocki)

    miejsca_ciecia = sorted(
        generator.sample(range(1, N), generator.randint(0, N - 1))
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

    return StanKlockow(podloza, wariant)