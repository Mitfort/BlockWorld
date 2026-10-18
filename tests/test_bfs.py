"""
Testy dla algorytmu BFS
"""
from src.algorytmy import bfs
from src.stan import StanKlockow
from pathlib import Path
from src.parser import Parser
from src.warianty import Warianty

DATA_DIR = Path(__file__).parent.parent / "data"

def test_bfs_simple():
    """
    Test the BFS algorithm with a simple case using the basic variant.
    """
    data_path = DATA_DIR / "test_sample.txt"

    # Parse the input data
    parser = Parser()
    start_dane, cel_dane = parser.parse(data_path=data_path)

    # start - [0, 1, 0, 2, 3], cel - [2, 3, 4, 5, 0]
    
    start = StanKlockow(start_dane, wariant=Warianty.PODSTAWOWY)
    cel = StanKlockow(cel_dane, wariant=Warianty.PODSTAWOWY)

    # Run BFS
    sekwencja, wezly, czas, sukces, _ = bfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    # Assertions
    assert sukces is True
    assert sekwencja is not None
    assert isinstance(sekwencja, list)
    assert all(isinstance(ruch, tuple) and len(ruch) == 2 for ruch in sekwencja)
    assert len(sekwencja) == 7

def test_bfs_extended():
    """
    Test the BFS with the extended variant.
    """
    data_path = DATA_DIR / "test_sample.txt"

    # Parse the input data
    parser = Parser()
    start_dane, cel_dane = parser.parse(data_path=data_path)

    start = StanKlockow(start_dane, wariant=Warianty.ROZSZERZONY)
    cel = StanKlockow(cel_dane, wariant=Warianty.ROZSZERZONY)

    # Run BFS
    sekwencja, wezly, czas, sukces, _ = bfs(
        start, cel, limit_wezlow=50000, limit_czasu=10.0
    )

    # Assertions
    assert sukces is True
    assert sekwencja is not None
    assert isinstance(sekwencja, list)
    assert all(isinstance(ruch, tuple) and len(ruch) == 2 for ruch in sekwencja)
    assert len(sekwencja) == 5