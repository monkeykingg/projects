from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "1", "2"), ("3", "4", "5"))
        >>> mnp1 = MNPuzzle(start_grid, target_grid)
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "1", "2"), ("3", "4", "5"))
        >>> mnp2 = MNPuzzle(start_grid, target_grid)
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "1"), ("3", "4", "5"))
        >>> mnp3 = MNPuzzle(start_grid, target_grid)
        >>> mnp1 == mnp2
        True
        >>> mnp1 == mnp3
        False
        """

        return type(other) == type(self) and \
            self.n == other.n and \
            self.m == other.m and \
            self.from_grid == other.from_grid and \
            self.to_grid == other.to_grid

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "1", "2"), ("3", "4", "5"))
        >>> a = MNPuzzle(start_grid, target_grid)
        >>> str(a) == '*12\\n345\\n'
        True
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "1"), ("3", "4", "5"))
        >>> b = MNPuzzle(start_grid, target_grid)
        >>> str(b) == '*21\\n345\\n'
        True
        """

        result = ''

        # Loop over all cells.
        for item in self.from_grid:
            for sub in item:
                result += sub
            result += '\n'

        return result

    def extensions(self):
        """
        Return list of legal extensions of Puzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "*"), ("4", "5", "3"))
        >>> mnp1 = MNPuzzle(start_grid, target_grid)
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mnp2 = MNPuzzle(start_grid, target_grid)
        >>> mnp2 in mnp1.extensions()
        True
        """

        # Extensions are configurations that can be reached by swapping one
        # symbol to the left, right, above, or below "*" with "*".

        # Use convenient names.
        from_grid, to_grid = self.from_grid, self.to_grid
        n, m = self.n, self.m

        # Accumulator.
        puzzles = []

        # Return empty list if it is impossible to get the answer.
        if self.from_grid == self.to_grid:
            return []

        # Loop over all cells and check if the cell is empty space.
        for i in range(n):
            for j in range(m):
                if from_grid[i][j] == '*':

                    # Swap empty space with up symbol if possible.
                    if i - 1 >= 0:
                        temp = [list(item) for item in from_grid]
                        temp[i][j], temp[i - 1][j] = temp[i - 1][j], temp[i][j]
                        puzzles.append(MNPuzzle(tuple([tuple(item[:])
                                                       for item in temp]),
                                                to_grid))

                    # Swap empty space with down symbol if possible.
                    if i + 1 < n:
                        temp = [list(item) for item in from_grid]
                        temp[i][j], temp[i + 1][j] = temp[i + 1][j], temp[i][j]
                        puzzles.append(MNPuzzle(tuple([tuple(item[:])
                                                       for item in temp]),
                                                to_grid))

                    # Swap empty space with left symbol if possible.
                    if j - 1 >= 0:
                        temp = [list(item) for item in from_grid]
                        temp[i][j], temp[i][j - 1] = temp[i][j - 1], temp[i][j]
                        puzzles.append(MNPuzzle(tuple([tuple(item[:])
                                                       for item in temp]),
                                                to_grid))

                    # Swap empty space with right symbol if possible.
                    if j + 1 < m:
                        temp = [list(item) for item in from_grid]
                        temp[i][j], temp[i][j + 1] = temp[i][j + 1], temp[i][j]
                        puzzles.append(MNPuzzle(tuple([tuple(item[:])
                                                       for item in temp]),
                                                to_grid))

                    return puzzles

    def is_solved(self):
        """
        Return True iff Puzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> MN = MNPuzzle(start_grid, target_grid)
        >>> MN.is_solved()
        False
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> MN = MNPuzzle(start_grid, target_grid)
        >>> MN.is_solved()
        True
        """

        # MNPuzzle is solved when from_grid is the same as to_grid.
        return self.from_grid == self.to_grid

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
