"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from grid_peg_solitaire_puzzle import GridPegSolitairePuzzle
from sudoku_puzzle import SudokuPuzzle
from mn_puzzle import MNPuzzle
from word_ladder_puzzle import WordLadderPuzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None

    >>> peg = GridPegSolitairePuzzle([['*','.'],['.','*']],{'.','*', '#'})
    >>> not depth_first_solve(peg)
    True
    >>> grid = ["1", "2", "3", "4"]
    >>> grid += ["3", "4", "1", "2"]
    >>> grid += ["2", "1", "4", "3"]
    >>> grid += ["4", "3", "2", "1"]
    >>> sudoku = SudokuPuzzle(4, grid, {"1", "2", "3", "4"})
    >>> type(depth_first_solve(sudoku)) == PuzzleNode
    True
    """

    # visit the puzzle
    # Add the str representation of it
    # to the visited_puzzles means it has already visited
    visited_puzzles = set()
    return _depth_first_puzzle_helper(puzzle, visited_puzzles)


def _depth_first_puzzle_helper(puzzle, visited_puzzles):
    # Help function that return the path of the puzzle node, when visit the
    # node, will append to the list to avoid visit it again
    #
    # @type puzzle: Puzzle
    # @type visited_puzzles: list[Puzzle]
    # @rtype: PuzzleNode | None

    # Visited puzzle, add the str of the puzzle to the set
    # and mean this puzzle has already visited
    # use str to avoid hashable problems
    visited_puzzles.add(str(puzzle))

    # Only return the node if it is not fail fast, if it is fail fast,
    # It will return None
    if not puzzle.fail_fast():

        #  Base Case, if the node don't have any extensions
        if not puzzle.extensions():
            # return the node if it is solved, if it is not solved,
            # It will return None, means, no solutions for this puzzle
            if puzzle.is_solved():
                return PuzzleNode(puzzle)

        else:
            # get the puzzle's extensions
            extensions = puzzle.extensions()
            # Make a node
            current_node = PuzzleNode(puzzle)
            for item in extensions:

                # avoid visiting twice
                if str(item) not in visited_puzzles:
                    deep_node = _depth_first_puzzle_helper(item,
                                                           visited_puzzles)
                    # determine if the path is available
                    if deep_node:

                        # if it has available path, leave one child left
                        # because a path only has one child
                        current_node.children = [deep_node]
                        deep_node.parent = current_node

                    # Return the node if the node has available path
                    if current_node.children:
                        return current_node


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None

    >>> mn = MNPuzzle((('1', '2'), ('*', '3')), (('1','2'), ('3','*')))
    >>> type(breadth_first_solve(mn)) == PuzzleNode
    True
    >>> word = WordLadderPuzzle('cat', 'dog', {'cat', 'dog', 'cot', 'cog'})
    >>> type(breadth_first_solve(word)) == PuzzleNode
    True
    """

    # Case that the puzzle has already solved
    if puzzle.is_solved():
        return PuzzleNode(puzzle)

    # The set which contains the str of the puzzle which has already visited
    # use str to avoid hashable problems
    visited_puzzles = {str(puzzle)}

    # Use the deque as a queue
    queue = deque()
    # Add the first node to the deque
    queue.append(PuzzleNode(puzzle))

    # Do the loop if the deque is not empty
    while len(queue) != 0:
        # Remove node from the left side of the deque, like dequeue
        temp = queue.popleft()
        # Get the puzzle's extensions
        extensions = temp.puzzle.extensions()

        # Check each puzzle's extension
        for item in extensions:
            # Check whether it is solved
            if item.is_solved():
                # Get the bottom node of the solution path
                solution = PuzzleNode(item, [], temp)
                # Push back to the top node
                # Since a path only has one children, so only leave one.
                while solution.parent:
                    solution.parent.children = [solution]
                    solution = solution.parent
                return solution

            # Append the node to the back if it is the puzzle hasn't visited
            # before
            if str(item) not in visited_puzzles:
                # Visit the extension puzzle and create the node which is
                # current node's children
                node = PuzzleNode(item, [], temp)
                temp.children.append(node)
                # Add the str representation to the set
                # and show that it has visited
                visited_puzzles.add(str(item))

        # Append all the children on the back of the deque, like enqueue
        # will visit the children later in order.
        for child in temp.children:
            queue.append(child)


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
