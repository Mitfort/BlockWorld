# Block World

Uruchomienie z katalogu `BlockWorld`:

```bash
python -m src.main test_sample.txt 1
python -m src.main test_sample.txt 2
```

Wariant `1` wymaga odłożenia klocka na stół przed przeniesieniem go na inny
klocek. Wariant `2` pozwala przenosić wolny klocek bezpośrednio na inny wolny
klocek. Program uruchamia DFS, BFS i IDA* oraz weryfikuje znalezione sekwencje.

## IDA*

Funkcja `ida_star` w `src/algorytmy.py` zwraca ten sam zestaw wyników co BFS:
sekwencję ruchów, liczbę rozwinięć węzłów, czas, status sukcesu i maksymalną
liczbę stanów przechowywanych na aktualnej ścieżce przeszukiwania.
Ruch `(klocek, podloze)` oznacza przeniesienie klocka na wskazane podłoże;
`0` oznacza stół.

Heurystyka `heurystyka_podloza(stan, cel)` liczy klocki, których bezpośrednie
podłoże różni się od docelowego:

```python
h = sum(a != b for a, b in zip(stan.podloza, cel.podloza, strict=True))
```

Przykładowo dla startu `[0, 1, 0]` i celu `[0, 3, 0]` heurystyka wynosi `1`:
tylko klocek `2` ma inne podłoże. W wariancie podstawowym potrzeba `2` ruchów
(`2` na stół, następnie na `3`), a w rozszerzonym `1` ruchu (`2` na `3`).

IDA* zaczyna od progu `h(start)` i wykonuje DFS z ograniczeniem
`f = g + h`, gdzie `g` to liczba wykonanych ruchów. Gałęzie z `f > prog`
są odcinane, a następny próg jest najmniejszą odciętą wartością `f`.
Zbiór stanów bieżącej ścieżki zapobiega cyklom i jest aktualizowany
przy cofaniu ruchów. Nie jest to globalny zbiór odwiedzonych stanów.

Każdy ruch zmienia podłoże dokładnie jednego klocka, więc może zmniejszyć
heurystykę najwyżej o `1`. Każdy klocek na błędnym podłożu trzeba przenieść
co najmniej raz. Heurystyka jest więc dopuszczalna i spójna; przy jednostkowym
koszcie ruchu IDA* zwraca najkrótszą sekwencję, jeżeli znajdzie rozwiązanie
w zadanych limitach. Poprawnie położony klocek również może wymagać
tymczasowego przeniesienia — heurystyka jest dolnym oszacowaniem.

Limity czasu i rozwinięć węzłów obejmują wszystkie iteracje łącznie.
Powtórne rozwinięcia są liczone ponownie; węzły odcięte przez próg nie są
liczone. Przekroczenie limitu zwraca `None` jako sekwencję i `False` jako
status sukcesu. Implementacja przechowuje stany bieżącej ścieżki i korzysta
z rekurencji Pythona.

Testy, w tym porównanie IDA* z BFS:

```bash
python -m pytest -q --tb=short
```

## Druga heurystyka: obowiązkowe ruchy

`heurystyka_obowiazkowych_ruchow(stan, cel)` wyznacza dla każdego klocka
dolne ograniczenie liczby koniecznych ruchów, a następnie je sumuje.
Klocek jest **ustalony**, jeśli cały jego łańcuch podłoży aż do stołu
zgadza się z układem docelowym. Dla klocka `b` liczymy:

- `0`, gdy jest ustalony;
- `2`, gdy nie jest ustalony, ale ma poprawne bezpośrednie podłoże;
- `2`, gdy w wariancie podstawowym jego aktualne i docelowe podłoże
  to dwa różne klocki;
- `1` w pozostałych przypadkach niezgodnego podłoża.

**Dopuszczalność.** Klocek na innym podłożu trzeba przenieść przynajmniej
raz. W wariancie podstawowym przejście z klocka na inny klocek musi prowadzić
przez stół, co wymaga przynajmniej dwóch ruchów tego samego klocka.
Jeśli bezpośrednie podłoże jest poprawne, ale klocek nie jest ustalony,
poniżej niego znajduje się klocek z błędnym podłożem. Aby go przestawić,
trzeba najpierw zdjąć wszystkie klocki nad nim. Rozpatrywany klocek musi
więc opuścić swoje podłoże, a potem na nie wrócić: co najmniej dwa ruchy.

Sumowanie jest bezpieczne, ponieważ ruch dotyczy dokładnie jednego klocka:
żaden ruch nie jest liczony w ograniczeniach dwóch różnych klocków.
Zatem `h2(stan) <= koszt_optymalny(stan)`. Ponadto `h2(cel) = 0` oraz
`h2(stan) >= h1(stan)`, gdzie `h1` to liczba błędnych podłoży.

Na przykład dla startu `[0, 1, 2]` i celu `[0, 0, 2]`:
`h1 = 1`, natomiast `h2 = 3`. Klocek `2` trzeba przestawić na stół,
a klocek `3` zdjąć z `2` i później na niego odłożyć.

Wybór heurystyki zachowuje dotychczasowy format wyniku:

```python
from src.algorytmy import ida_star, heurystyka_obowiazkowych_ruchow

sekwencja, wezly, czas, sukces, pamiec = ida_star(
    start, cel, limit_wezlow=30000,
    heurystyka=heurystyka_obowiazkowych_ruchow,
)
```

## Porównanie heurystyk

Uruchomienie badania dla `N in {6, 8, 10, 12, 15}`, po pięć losowych
problemów na rozmiar, w obu wariantach ruchów:

```bash
python -m src.porownanie_heurystyk --limit-wezlow 30000 --output-dir wyniki/nowe_porownanie
```

Opcja `--wariant 1` lub `--wariant 2` ogranicza badanie do jednego wariantu.
Można także podać `--ziarno`, `--rozmiary` i `--problemow`.
Katalog wynikowy musi być nowy, żeby nie nadpisać wcześniejszych pomiarów.

Obie heurystyki dostają dokładnie te same stany i kolejność ruchów.
Ziarno problemu to `20261019 + 100 * N + numer_problemu` (numery od 1).
Ten sam zestaw układów jest też używany w obu wariantach. Generator losuje
permutację klocków i podział na wieże; rozkład nie jest jednostajny po stanach.
Limit czasu jest wyłączony, a limit rozwinięć dotyczy całego IDA*, łącznie
ze wszystkimi iteracjami. Przebiegi odbywają się kolejno, po krótkiej
rozgrzewce, ze zmienną kolejnością heurystyk.

Wyniki zawierają:

- `raport.html`: wykresy, zestawienia, uzasadnienie dopuszczalności i filtry;
- `wyniki.csv`: liczba rozwinięć, czas, długości i porównanie dla każdego problemu;
- `wyniki.json`: pełna konfiguracja, podsumowania, stany i sekwencje ruchów;
- `przebieg.jsonl`: zapis zakończonych par wyników w trakcie badania.

Każda znaleziona sekwencja jest weryfikowana zgodnie z wariantem ruchów.
Długości porównujemy wyłącznie wtedy, gdy **obie** heurystyki znalazły
rozwiązanie. Dwa niepowodzenia nie są traktowane jako równe długości.
Raport pokazuje średnie po wszystkich próbach, z oznaczeniem limitów,
oraz osobno średnie na wspólnie rozwiązanych problemach.
Pomiar czasu obejmuje przeszukiwanie i obliczanie heurystyki, bez generowania,
weryfikacji i zapisu. Jest to jeden pomiar na przebieg, więc zwłaszcza
różnice dla bardzo krótkich czasów mogą wynikać z obciążenia systemu.

Zapisane badanie: `wyniki/heurystyki_ida_star_20261019/raport.html`.

Eksport wykresów do PNG i SVG (korzysta z matplotlib):

```bash
python -m src.wykres_heurystyk wyniki/heurystyki_ida_star_20261019/wyniki.json
```

W zapisanym badaniu h1 rozwiązała 19/25 problemów w wariancie podstawowym
i 20/25 w rozszerzonym; h2 odpowiednio 25/25 i 23/25. We wszystkich 39
przypadkach wspólnego sukcesu długości sekwencji były identyczne.
Pozostałe 11 par nie pozwala porównać długości z powodu limitu.
H2 potrzebowała mniej rozwinięć, ale nie zawsze mniej czasu: dla N=15
w wariancie rozszerzonym średni czas wszystkich prób był wyższy z h2,
ponieważ dwa przebiegi także doszły do limitu, a jej obliczanie jest droższe.
