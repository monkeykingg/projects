from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Check whether the two WordLadderPuzzle are the same.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> a = WordLadderPuzzle('bit', 'bat', {'bit', 'bat'})
        >>> b = WordLadderPuzzle('bit', 'bat', {'bit', 'bat'})
        >>> c = WordLadderPuzzle('dig', 'big', {'dig', 'big'})
        >>> a == b
        True
        >>> c == b
        False
        """

        return type(self) == type(other) and self._from_word == \
            other._from_word and self._to_word == other._to_word

    def __str__(self):
        """
        The string representation of the puzzle

        @type self: WordLadderPuzzle
        @rtype: str

        >>> a = WordLadderPuzzle('bit', 'bat', {'bit', 'bat'})
        >>> str(a) == 'bit->bat'
        True
        >>> b = WordLadderPuzzle('dig', 'big', {'dig', 'big'})
        >>> str(b) == 'dig->big'
        True
        """

        return '{}->{}'.format(self._from_word, self._to_word)

    def extensions(self):
        """
        Return list of possibilities of the next step

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> a = WordLadderPuzzle('bit', 'bat', {'bit', 'bat'})
        >>> a.extensions() == [WordLadderPuzzle('bat', 'bat', {'bit', 'bat'})]
        True
        >>> b = WordLadderPuzzle('dig', 'big', {'dig', 'big'})
        >>> b.extensions() == [WordLadderPuzzle('big', 'big', {'dig', 'big'})]
        True
        """

        # Use convenient name.
        from_word, to_word, ws = self._from_word, self._to_word, self._word_set
        chars = self._chars

        # Accumulators.
        new_words = []
        puzzles = []

        # Return empty list if it is impossible to get the answer.
        if to_word not in ws or len(from_word) != len(to_word):
            return []

        # If the from word is an answer return the empty list.
        if self.is_solved():
            return []

        # Change one letter for each position of one word.
        for i in range(0, len(from_word)):
            for j in range(0, len(chars)):
                new_word = from_word[0:i] + chars[j] + from_word[i + 1:]

                # Get the new word if it is in the word set and it
                # is not the same as the from word.
                if new_word in ws and new_word != from_word:
                    new_words.append(new_word)

        # Get the new puzzle and append to the list
        # which from all the possibility of the next word.
        for item in new_words:
            puzzles.append(WordLadderPuzzle(item, to_word, ws))

        return puzzles

    def is_solved(self):
        """
        Check whether the WordLadderPuzzle is solved or not

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> a = WordLadderPuzzle('bat', 'bat', {'bit', 'bat'})
        >>> a.is_solved()
        True
        >>> b = WordLadderPuzzle('bit', 'bat', {'bit', 'bat'})
        >>> b.is_solved()
        False
        """

        # It is solved if the from word is the same as the to word.
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
