from typing import Generator, List, Tuple

from .dictionary import Dictionary


class BoggleGrid:
    # Assumption: letter_grid is non-empty, contains atleast one letter
    def __init__(self, letter_grid: List[List[str]], dictionary: Dictionary) -> None:
        self.dictionary = dictionary
        self.letter_grid = letter_grid
        self.grid_height = len(letter_grid)
        self.grid_length = len(letter_grid[0])

    def _traverse_from_node(
        self,
        row: int,
        col: int,
        prefix: str = "",
        visited_nodes: List[Tuple[int, int]] = None,
    ) -> Generator[str, None, None]:
        visited_nodes = visited_nodes or []

        if (row, col) in visited_nodes:
            return

        prefix += self.letter_grid[row][col]
        if self.dictionary.is_word(prefix):
            yield prefix

        for adj_row, adj_col in self._get_adjacent_nodes(row=row, col=col):
            if (adj_row, adj_col) in visited_nodes:
                continue
            # Create a new list of visited nodes including (row, col) tuple for this iteration.
            # It is important to not mutate 'visited_nodes' list because each iteration is supposed to
            # branch out to find words independenty and can share nodes as part of different words
            visited_nodes_for_iteration = visited_nodes + [(row, col)]
            for word in self._traverse_from_node(
                row=adj_row,
                col=adj_col,
                visited_nodes=visited_nodes_for_iteration,
                prefix=prefix,
            ):
                yield word

    def _get_adjacent_nodes(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Return adjacent nodes for a given node"""
        adjacent_nodes = []

        for adj_row in range(max(0, row - 1), min(row + 2, self.grid_height)):
            for adj_col in range(max(0, col - 1), min(col + 2, self.grid_length)):
                if row != adj_row or col != adj_col:
                    adjacent_nodes.append((adj_row, adj_col))

        return adjacent_nodes

    def traverse(self) -> Generator[str, None, None]:
        """Traverse the Boggle Grid and find matched words"""
        for i in range(self.grid_height):
            for j in range(self.grid_length):
                for word in self._traverse_from_node(row=i, col=j):
                    yield word
