from pathlib import Path
from typing import Tuple 

class Parser:
    def parse(self, data_path: Path) -> Tuple[list[int], list[int]]: 
        """
        Parse the data from the specified path.
        """
        if not data_path.exists():
            raise FileNotFoundError(f"File not found: {data_path}")

        with data_path.open("r") as file:
            data = file.read()

        parsed_data = self._process_data(data)
        return parsed_data

    def _process_data(self, data: str) -> Tuple[list[int], list[int]]:
        """
        From the raw data return start and goal sequences
        """
        start_seq: list[int] = []
        goal_seq: list[int] = []

        for line in data.splitlines():
            if line[0] == '#' or not line.strip():
                continue # Skip comment lines 

            if not start_seq: 
                start_seq = [int(x) for x in line.split()]

            else:
                goal_seq = [int(x) for x in line.split()]


        return start_seq, goal_seq
