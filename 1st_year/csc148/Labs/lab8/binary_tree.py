class BinaryTree:
    """
    A Binary Tree, i.e. arity 2.

    === Attributes ===
    @param object data: data for this binary tree node
    @param BinaryTree|None left: left child of this binary tree node
    @param BinaryTree|None right: right child of this binary tree node
    """

    def __init__(self, data, left=None, right=None):
        """
        Create BinaryTree self with data and children left and right.

        @param BinaryTree self: this binary tree
        @param object data: data of this node
        @param BinaryTree|None left: left child
        @param BinaryTree|None right: right child
        @rtype: None
        """
        self.data, self.left, self.right = data, left, right

    def __eq__(self, other):
        """
        Return whether BinaryTree self is equivalent to other.

        @param BinaryTree self: this binary tree
        @param Any other: object to check equivalence to self
        @rtype: bool

        >>> BinaryTree(7).__eq__("seven")
        False
        >>> b1 = BinaryTree(7, BinaryTree(5))
        >>> b1.__eq__(BinaryTree(7, BinaryTree(5), None))
        True
        """
        return (type(self) == type(other) and
                self.data == other.data and
                (self.left, self.right) == (other.left, other.right))

    def __repr__(self):
        """
        Represent BinaryTree (self) as a string that can be evaluated to
        produce an equivalent BinaryTree.

        @param BinaryTree self: this binary tree
        @rtype: str

        >>> BinaryTree(1, BinaryTree(2), BinaryTree(3))
        BinaryTree(1, BinaryTree(2, None, None), BinaryTree(3, None, None))
        """
        return "BinaryTree({}, {}, {})".format(repr(self.data),
                                               repr(self.left),
                                               repr(self.right))

    def __str__(self, indent=""):
        """
        Return a user-friendly string representing BinaryTree (self)
        inorder.  Indent by indent.

        >>> b = BinaryTree(1, BinaryTree(2, BinaryTree(3)), BinaryTree(4))
        >>> print(b)
            4
        1
            2
                3
        <BLANKLINE>
        """
        right_tree = (self.right.__str__(
            indent + "    ") if self.right else "")
        left_tree = self.left.__str__(indent + "    ") if self.left else ""
        return (right_tree + "{}{}\n".format(indent, str(self.data)) +
                left_tree)

    def __contains__(self, value):
        """
        Return whether tree rooted at node contains value.

        @param BinaryTree self: binary tree to search for value
        @param object value: value to search for
        @rtype: bool

        >>> BinaryTree(5, BinaryTree(7), BinaryTree(9)).__contains__(7)
        True
        """
        return (self.data == value or
                (self.left and value in self.left) or
                (self.right and value in self.right))


def parenthesize(b):
    """
    Return a parenthesized expression equivalent to the arithmetic
    expression tree rooted at b.

    Assume:  -- b is a binary tree
             -- interior nodes contain data in {'+', '-', '*', '/'}
             -- interior nodes always have two children
             -- leaves contain float data

    @param BinaryTree b: arithmetic expression tree
    @rtype: str

    >>> b1 = BinaryTree(3.0)
    >>> print(parenthesize(b1))
    3.0
    >>> b2 = BinaryTree(4.0)
    >>> b3 = BinaryTree(7.0)
    >>> b4 = BinaryTree("*", b1, b2)
    >>> b5 = BinaryTree("+", b4, b3)
    >>> print(parenthesize(b5))
    ((3.0 * 4.0) + 7.0)
    """
    if isinstance(b.data, str):
        return str("(" + parenthesize(b.left) + " " + b.data + " " + parenthesize(b.right) + ")")
    if isinstance(b.data, float):
        return str(b.data)


def all_path(node):
    """

    @param node:
    @type node:
    @return:
    @rtype:

    >>> all_path(None)
    []
    >>> all_path(BinaryTree(5))
    [[5]]
    >>> b1 = BinaryTree(7)
    >>> b2 = BinaryTree(3, BinaryTree(2), None)
    >>> b3 = BinaryTree(5, b2, b1)
    >>> all_path(b3)
    [[5, 3, 2], [5, 7]]
    """
    if not node:
        return []

    if not node.left and not node.right:
        return [[node.data]]

    acc = []
    for c in [node.left, node.right]:
        for path in all_path(c):
            acc.append([node.data] + path)
    return acc


def list_longest_path(node):
    """
    List the data in a longest path of node.

    @param BinaryTree|None node: tree to list longest path of
    @rtype: list[object]

    >>> list_longest_path(None)
    []
    >>> list_longest_path(BinaryTree(5))
    [5]
    >>> b1 = BinaryTree(7)
    >>> b2 = BinaryTree(3, BinaryTree(2), None)
    >>> b3 = BinaryTree(5, b2, b1)
    >>> list_longest_path(b3)
    [5, 3, 2]
    """
    acc = all_path(node)
    if not acc:
        return []
    temp = []
    for x in acc:
        temp.append(len(x))
    longest = max(temp)
    i = temp.index(longest)
    return acc[i]


def insert(node, data):
    """
    Insert data in BST rooted at node if necessary, and return new root.

    Assume node is the root of a Binary Search Tree.

    @param BinaryTree node: root of a binary search tree.
    @param object data: data to insert into BST, if necessary.

    >>> b = BinaryTree(5)
    >>> b1 = insert(b, 3)
    >>> print(b1)
    5
        3
    <BLANKLINE>
    """
    return_node = node
    if not node:
        return_node = BinaryTree(data)
    elif data < node.data:
        node.left = insert(node.left, data)
    elif data > node.data:
        node.right = insert(node.right, data)
    else:  # nothing to do
        pass
    return return_node


def list_between(node, start, end):
    """
    Return a Python list of all values in the binary search tree
    rooted at node that are between start and end (inclusive).

    @param BinaryTree|None node: binary tree to list values from
    @param object start: starting value for list
    @param object end: stopping value for list
    @rtype: list[object]

    >>> list_between(None, 3, 13)
    []
    >>> b = BinaryTree(8)
    >>> b = insert(b, 4)
    >>> b = insert(b, 2)
    >>> b = insert(b, 6)
    >>> b = insert(b, 12)
    >>> b = insert(b, 14)
    >>> b = insert(b, 10)
    >>> list_between(b, 2, 3)
    [2]
    >>> L = list_between(b, 3, 11)
    >>> L.sort()
    >>> L
    [4, 6, 8, 10]
    """
    if not node:
        return []

    acc = []

    # Only check left if still in bound
    if node.data > start:
        acc += list_between(node.left, start, end)

    # Check node.data
    if start <= node.data <= end:
        acc += [node.data]

    # Only check right if still in bound
    if node.data < end:
        acc += list_between(node.right, start, end)

    return acc

def bst_del_rec(tree, data):
    """

    @type tree: BinaryTree
    @type data: data
    @rtype:

    >>> bst_del_rec(None, 1)
    None
    >>> bst_del_rec(BinaryTree(5), 5)
    []
    >>> b1 = BinaryTree(7)
    >>> b2 = BinaryTree(3, BinaryTree(2), None)
    >>> b3 = BinaryTree(5, b2, b1)
    >>> b4 = BinaryTree(5, BinaryTree(2), BinaryTree(7))
    >>> b5 = BinaryTree(7, BinaryTree(8), BinaryTree(6))
    >>> b6 = BinaryTree(6, BinaryTree(8), None)
    >>> b7 = BinaryTree(5, b2, b5)
    >>> b8 = BinaryTree(5, b2, b6)
    >>> bst_del_rec(b3, 3) == b4
    True
    >>> bst_del_rec(b7, 7) == b8
    True
    """

    # Base case.
    if not tree:
        return None

    # Recursive case 1.
    if data < tree.data:
        tree.left = bst_del_rec(tree.left, data)

    # Recursive case 2.
    if data > tree.data:
        tree.right = bst_del_rec(tree.right, data)

    if tree.left is None:
        return tree.right

    else:
        largest = findmax(tree.left)
        tree.data = largest.data
        tree.left = bst_del_rec(tree.left, largest.data)
        return tree

def findmax(tree):
    return tree if not tree.right else findmax(tree.right)

def swap_child(t):
    """

    @type t:
    @rtype:

    >>> b1 = BinaryTree(7)
    >>> b2 = BinaryTree(3)
    >>> b3 = BinaryTree(5, b2, b1)
    >>> swap_child(b3)
    >>> b3 == BinaryTree(5, b1, b2)
    True
    """
    if not t:
        return
    if not t.left and not t.right:
        return
    if t.left or t.right:
        t.left, t.right = t.right, t.left
    for c in [t.left, t.right]:
        swap_child(c)
    return


if __name__ == "__main__":
    import doctest
    doctest.testmod()
