#stan.py
class StanKlockow:
    def __init__(self, podloza: list [int]):
        self.podloza = podloza
        self.N=len(podloza)
    
    
    def funkcjaWalidacyjna(self) -> tuple[bool, str]:
        #sprawdzamy, czy v nie jest na nieistniejącym bloczku
        for v in self.podloza:
            if v < 0 or v > self.N:
                return False, "Blad ulozenia"

        #sprawdzamy czy nie jest sam na sobie
        for v, podloze in enumerate(self.podloza, start = 1):
            if v == podloze:
                return False, "v lezy sam na sobie"

        #sprawdzamy, czy dwa klocki nie leżą na tym samym klocku
        indeksy=[]
        for v in self.podloza:
            if v == 0:
                continue
            else:
                if v not in indeksy:
                    indeksy.append(v)
                else:
                    return False, "dwa klocki leżą na tym samym klocku"

        #sprawdzamy czy nie ma cykli

        for v in range(1, self.N + 1):
            odwiedzone = set()
            aktualny = v

            while aktualny !=0:
                if aktualny in odwiedzone:
                    return False, "wykryto cykl"
                odwiedzone.add(aktualny)
                aktualny= self.podloza[aktualny-1]

        return True, "uklad poprawny"

    def wolneKlocki(self) -> list[int]:
        zajete = set(self.podloza)
        wolne =[]
        for v in range (1, self.N + 1):
            if v not in zajete:
                wolne.append(v)
        return wolne

    def generuj_ruchy(self) ->list[tuple[int,int]]:
        wolne = self.wolneKlocki()
        ruchy=[]

        for v in wolne:
            obecne_podloze = self.podloza[v-1]
            if obecne_podloze != 0:
                ruchy.append((v,0))
            elif obecne_podloze == 0:
                for cel in wolne:
                    if cel != v:
                        ruchy.append((v,cel))
        return ruchy

    def wykonajRuch(self, ruch: tuple[int,int]) -> "StanKlockow":
        v, cel = ruch

        nowe_podloze = list(self.podloza)

        nowe_podloze[v - 1] = cel

        return StanKlockow(nowe_podloze)
