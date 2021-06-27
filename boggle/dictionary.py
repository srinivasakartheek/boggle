from abc import ABC, abstractmethod


class Dictionary(ABC):
    @abstractmethod
    def is_word(self, possible_word: str) -> bool:
        raise NotImplementedError


class FileBasedDictionary:
    # Assumption: It is okay to load all the words into memory. If we are constrained by memory,
    # we can read all the words starting with few character(starting with 'a', 'b', 'c'), find the
    # starting letters on the grid and traverse from those letters and do a scoped finding and repeat
    # till we read all words from the dictionary
    def __init__(self, file_path: str) -> None:
        with open(file_path, "r") as f:
            # Save the words in a set because the only function this dictionary supports is
            # to lookup the whole word and lookups are faster for a set. If the dictionary needs to support
            # more functions like matching and searching, we should use a Trie data structure
            self.words = frozenset(word.rstrip("\n").upper() for word in f.readlines() if not word.startswith("#"))

    def is_word(self, possible_word: str) -> bool:
        return possible_word.upper() in self.words
