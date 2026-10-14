"""
Test parser functionality.
"""

from pathlib import Path
from src.parser import Parser

data_dir = Path(__file__).parent.parent / "data"

def test_parser():
    """
    Test the parser function with sample data.
    """
    parser = Parser()
    result = parser.parse(data_path=data_dir / "test_sample.txt")

    assert result == ([0, 1, 0, 2, 3], [2, 3, 4, 5, 0]) 