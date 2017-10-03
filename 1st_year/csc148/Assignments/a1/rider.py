from location import Location
"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """
    The type that represents people who wants drivers to drive them to certain
    destination. The person has user id as identifier, the origin, the
    destination, and the patience of the person.

    === Attributes ===
    @type id: str
        The user id, which is the unique identifier
    @type origin: tuple of int
        The location of the current location of the rider
    @type destination: tuple of int
        The location that the rider wants to go
    @type patience: int
        The time rider can wait before the cancellation of the ride
    @type status: str
        The status of the rider
    """

    def __init__(self, identification, origin, destination, patience):
        """Initialize the new rider

        @type self: Rider
        @type identification: str
        @type origin: Location
        @type destination: Location
        @type patience: int
        @rtype: None
        """
        self.id = identification
        self.origin = origin
        self.destination = destination
        self.patience = patience
        self.status = WAITING

    def __str__(self):
        """The string representation of the rider

        @type self: Rider
        @rtype: str
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> str(Peter)
        'Peter'
        >>> James = Rider('James', Location(4,9), Location(3,6), 3)
        >>> str(James)
        'James'
        """
        return self.id

    def __eq__(self, other):
        """Show that the user are the same by comparing the user id

        @type self: Rider
        @type other: Rider | Any
        @rtype: bool
        >>> a = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> b = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> c = Rider('James', Location(4,9), Location(3,6), 3)
        >>> a == b
        True
        >>> a == c
        False
        """
        return type(self) == type(other) and self.id == other.id
