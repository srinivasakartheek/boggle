#! /usr/bin/env python
import re
import sys
from datetime import datetime
from typing import List, Optional

from boggle import BoggleGrid, FileBasedDictionary


def main(letter_grid: List[List[str]]):
    dictionary = FileBasedDictionary(file_path="american-english-large.txt")
    boggle_grid = BoggleGrid(
        letter_grid=letter_grid,
        dictionary=dictionary,
    )
    print("Finding words...")
    start = datetime.now()
    matches = {word for word in boggle_grid.traverse()}
    end = datetime.now()
    print(f"Found {len(matches)} unique word(s) in {round((end-start).total_seconds(), 2)}s. Writing to matches.txt")
    with open("matches.txt", "w") as f:
        f.write("\n".join(matches))


def get_grid_dimension(val: str) -> Optional[int]:
    try:
        dimension = int(val)
        if dimension > 0:
            return dimension
    except ValueError:
        pass

    return None


if __name__ == "__main__":
    grid_length = get_grid_dimension(input("Enter length of the grid: "))
    if grid_length is None:
        print("Grid Length must be a positive integer")
        sys.exit(1)

    grid_height = get_grid_dimension(input("Enter height of the grid: "))
    if grid_height is None:
        print("Grid Height must be a positive integer")
        sys.exit(1)

    letter_grid = []
    grid_row_regex = re.compile(rf"^[a-zA-z]{{{grid_length}}}$")
    for i in range(grid_height):
        row = input(f"Enter row #{i+1} (without any spaces): ")
        if re.match(grid_row_regex, row):
            letter_grid.append([c.upper() for c in row])
        else:
            print(f"Row must and only contain exactly {grid_length} alphabets")
            sys.exit(1)

    main(letter_grid=letter_grid)
