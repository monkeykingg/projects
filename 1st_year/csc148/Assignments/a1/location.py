class Location:
    """ This class Locaiton represent the type which represent locations

    === Attributes ===
    @type row: int
        The row of the location
    @type column: int
        The column of the location
    """

    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        self.row = row
        self.column = column

    def __str__(self):
        """Return a string representation.

        @rtype: str
        >>> a = Location(1, 2)
        >>> str(a)
        '(1, 2)'
        >>> b = Location(3, 4)
        >>> str(b)
        '(3, 4)'
        """
        return "({}, {})".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool
        """
        # Check the type first, then check whether the rows and columns are the
        # same as the other's
        return (type(self) == type(other) and
                self.row == other.row and
                self.column == other.column)


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    >>> a = Location(1, 2)
    >>> b = Location(3, 4)
    >>> manhattan_distance(a, b)
    4
    >>> c = Location(2, 4)
    >>> d = Location(3, 9)
    >>> manhattan_distance(c, d)
    6
    """
    # The location is calulated by the sum of the difference of the two rows,
    # and the difference of the two columns
    return abs(destination.row - origin.row) + \
        abs(destination.column - origin.column)


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    >>> a = deserialize_location('2,4')
    >>> a.row
    2
    >>> a.column
    4
    >>> b = deserialize_location('3,5')
    >>> b.row
    3
    >>> b.column
    5
    """
    # Convert the string to a two-element list
    loc = location_str.split(',')

    # The first element is row, the second is col
    return Location(int(loc[0]), int(loc[1]))
