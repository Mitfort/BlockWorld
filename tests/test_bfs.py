"""
Testy dla algorytmu BFS
"""
from src.algorytmy import bfs
from src.stan import StanKlockow
from pathlib import Path
from src.parser import Parser

DATA_DIR = Path(__file__).parent.parent / "data"

def test_bfs():
    """
    Test the BFS algorithm with a sample input.
    """
    data_path = DATA_DIR / "test_sample.txt"

    # Parse the input data
    parser = Parser()
    start_dane, cel_dane = parser.parse(data_path=data_path)

    # start - [0, 1, 0, 2, 3], cel - [2, 3, 4, 5, 0]
    
    start = StanKlockow(start_dane)
    cel = StanKlockow(cel_dane)

    # Run BFS
    sekwencja, wezly, czas, sukces = bfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    # Assertions
    assert sukces is True
    assert sekwencja is not None
    assert isinstance(sekwencja, list)
    assert all(isinstance(ruch, tuple) and len(ruch) == 2 for ruch in sekwencja)