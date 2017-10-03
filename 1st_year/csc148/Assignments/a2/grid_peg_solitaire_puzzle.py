from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", "*", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", "*", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", "*", ".", "*", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp3 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp1 == gpsp2
        True
        >>> gpsp2 == gpsp3
        False
        """

        return type(self) == type(other) and\
            self._marker == other._marker and\
            self._marker_set == other._marker_set

    def __str__(self):
        """
        Return a human-readable string representation of
        GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", "*", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> a = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> str(a) == '. . . . . \\n. . . . . ' + \
        '\\n. . . * . \\n. . . . . \\n. . . . . \\n'
        True
        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", "*", ".", "*", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> b = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> str(b) == '. . . . . \\n. . . . . ' + \
        '\\n. * . * . \\n. . . . . \\n. . . . . \\n'
        True
        """

        result = ''

        # Loop over all cells.
        for i in self._marker:
            for j in i:
                result += (j + ' ')
            result += '\n'

        return result

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", "*", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.extensions()
        []
        >>> grid1 = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", "*", "*"],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", "*", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2 in gpsp1.extensions()
        True
        """

        # Extensions consist of all configurations that can be reached by
        # making a single jump from this configuration.

        # Use convenient names.
        marker, marker_set = self._marker, self._marker_set

        # Accumulator.
        puzzles = []

        # Return empty list if it is impossible to get the answer.
        if self.is_solved():
            return []

        # Loop over all cells.
        for i in range(len(marker)):
            for j in range(len(marker[i])):
                if marker[i][j] == '.':

                    # Peg jumps from up if possible.
                    if i - 2 >= 0 and marker[i - 2][j] ==\
                            marker[i - 1][j] == '*':
                        temp = [item[:] for item in marker]
                        temp[i][j], temp[i - 1][j], \
                            temp[i - 2][j] = '*', '.', '.'
                        puzzles.append(GridPegSolitairePuzzle(temp,
                                                              marker_set))

                    # Peg jumps from down if possible.
                    if i + 2 < len(marker) and marker[i + 2][j] ==\
                            marker[i + 1][j] == '*':
                        temp = [item[:] for item in marker]
                        temp[i][j], temp[i + 1][j],\
                            temp[i + 2][j] = '*', '.', '.'
                        puzzles.append(GridPegSolitairePuzzle(temp,
                                                              marker_set))

                    # Peg jumps from left if possible.
                    if j - 2 >= 0 and marker[i][j - 2] ==\
                            marker[i][j - 1] == '*':
                        temp = [item[:] for item in marker]
                        temp[i][j], temp[i][j - 1], \
                            temp[i][j - 2] = '*', '.', '.'
                        puzzles.append(GridPegSolitairePuzzle(temp,
                                                              marker_set))

                    # Peg jumps from right if possible.
                    if j + 2 < len(marker[i]) and marker[i][j + 2] ==\
                            marker[i][j + 1] == '*':
                        temp = [item[:] for item in marker]
                        temp[i][j], temp[i][j + 1],\
                            temp[i][j + 2] = '*', '.', '.'
                        puzzles.append(GridPegSolitairePuzzle(temp,
                                                              marker_set))

        return puzzles

    def is_solved(self):
        """
        Return True iff Puzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", "*", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        True
        >>> grid = [[".", ".", ".", ".", "."],
        ...   [".", ".", ".", ".", "."],
        ...   [".", ".", ".", "*", "."],
        ...   [".", "*", ".", ".", "."],
        ...   [".", ".", ".", ".", "."]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        False
        """

        # It is solved if there is exactly one "*" left.
        count = 0
        for item in self._marker:
            for obj in item:
                if obj == "*":
                    count += 1
        return count == 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
