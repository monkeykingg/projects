from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    # === Private Attributes ===
    # @type _speed: int
    #   The speed of the car only the driver knows
    # @type _destination: Location | None
    #     If the rider is assigned by the driver, this will be the the locaiton
    #     of the current rider. It will be rider's destination if the ride
    #     starts. It will be None if and only if the driver is idle

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        self.id = identifier
        self.location = location
        self._speed = speed
        self.is_idle = True
        self._destination = None

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str
        >>> Peter = Driver('Peter', Location(2, 3), 4)
        >>> str(Peter)
        'Peter'
        >>> David = Driver('David', Location(5, 3), 2)
        >>> str(David)
        'David'
        """
        return self.id

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool
        >>> a = Driver('Peter', Location(2, 3), 4)
        >>> b = Driver('Peter', Location(2, 3), 4)
        >>> c = Driver('David', Location(5, 3), 2)
        >>> a == b
        True
        >>> a == c
        False
        """
        return type(self) == type(other) and self.id == other.id

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int
        >>> a = Driver('Peter', Location(2, 3), 4)
        >>> a.get_travel_time(Location(3, 6))
        1
        >>> b = Driver('David', Location(5, 3), 2)
        >>> b.get_travel_time(Location(1, 7))
        4
        """
        # Get the distance between two locations.
        distance = manhattan_distance(self.location, destination)
        # Get the time by divide distance by speed, and round it to the nearest
        # integer
        time = round(distance / self._speed)
        return time

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        >>> a = Driver('Peter', Location(2, 3), 4)
        >>> a.is_idle
        True
        >>> a.start_drive(Location(3, 6))
        1
        >>> a.is_idle
        False
        >>> b = Driver('David', Location(5, 3), 2)
        >>> b.is_idle
        True
        >>> b.start_drive(Location(1, 7))
        4
        >>> b.is_idle
        False
        """
        # Driver will not be idle if the driver starts drive
        self.is_idle = False

        # Set driver's destination
        self._destination = location

        # Get the time
        return self.get_travel_time(self._destination)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        >>> a = Driver('Peter', Location(2, 3), 4)
        >>> str(a.location)
        '(2, 3)'
        >>> a.start_drive(Location(3, 6))
        1
        >>> a.end_drive()
        >>> a.location == Location(3, 6)
        True
        >>> b = Driver('David', Location(5, 3), 2)
        >>> b.location == Location(5, 3)
        True
        >>> b.start_drive(Location(1, 7))
        4
        >>> b.end_drive()
        >>> b.location == Location(1, 7)
        True
        """
        self.location = self._destination
        self.is_idle = True
        self._destination = None

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int
        >>> a = Driver('Peter', Location(2, 3), 1)
        >>> a.start_ride(Rider('Tom', Location(1, 2), Location(3, 4), 10))
        4
        >>> a.location == Location(1, 2)
        True
        >>> b = Driver('Allen', Location(1, 1), 2)
        >>> b.start_ride(Rider('Mark', Location(2, 3), Location(5, 6), 9))
        3
        >>> b.location == Location(2, 3)
        True
        """
        # Driver is at rider's location and drive the rider's destination
        self.location = rider.origin
        self.is_idle = False
        self._destination = rider.destination

        # Get the time
        return self.get_travel_time(self._destination)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        >>> a = Driver('Peter', Location(2, 3), 1)
        >>> a.start_ride(Rider('Tom', Location(1, 2), Location(3, 4), 10))
        4
        >>> a.end_ride()
        >>> a.location == Location(3, 4)
        True
        >>> a.is_idle
        True
        >>> b = Driver('Allen', Location(1, 1), 2)
        >>> b.start_ride(Rider('Mark', Location(2, 3), Location(5, 6), 9))
        3
        >>> b.end_ride()
        >>> b.location == Location(5, 6)
        True
        >>> b.is_idle
        True
        """
        # The driver arrived at the rider's destination
        self.location = self._destination
        self._destination = None
        self.is_idle = True
