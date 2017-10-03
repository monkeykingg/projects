"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF
from location import Location


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> event = Event(0)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_request = RiderRequest(event.timestamp, Peter)
        >>> print(rider_request.do(dispatcher, monitor)[0])
        2 -- Peter: Cancel request
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)
        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        >>> event = Event(2)
        >>> Tom = Rider('Tom', Location(2, 4), Location(3, 4), 6)
        >>> rider_request = RiderRequest(event.timestamp, Tom)
        >>> str(rider_request)
        '2 -- Tom: Request a driver'
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> event_1 = Event(7)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> dispatcher_1 = Dispatcher()
        >>> monitor_1 = Monitor()
        >>> driver_request_1 = DriverRequest(event_1.timestamp, David)
        >>> driver_request_1.do(dispatcher_1, monitor_1)
        []
        >>> dispatcher_1.request_driver(Peter) == David
        True
        """
        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)
        events = []
        # Request a rider from the dispatcher.
        rider = dispatcher.request_rider(self.driver)

        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 rider, self.driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        >>> event_1 = Event(7)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> driver_request_1 = DriverRequest(event_1.timestamp, David)
        >>> str(driver_request_1)
        '7 -- David: Request a rider'
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """A cancellation changes a waiting rider to a cancelled rider.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a Cancellation event.

        @type self: Cancellation
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def __str__(self):
        """Return a string representation of this event.

        @type self: Cancellation
        @rtype: str
        >>> event_1 = Event(7)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> cancellation_1 = Cancellation(event_1.timestamp, Peter)
        >>> str(cancellation_1)
        '7 -- Peter: Cancel request'
        """
        return "{} -- {}: Cancel request".format(self.timestamp, self.rider)

    def do(self, dispatcher, monitor):
        """Register the rider.

        If the rider has already been picked up, then they are satisfied and
        cannot be cancelled.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> event_1 = Event(7)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> cancellation_1 = Cancellation(event_1.timestamp, Peter)
        >>> dispatcher_1 = Dispatcher()
        >>> monitor_1 = Monitor()
        >>> cancellation_1.do(dispatcher_1, monitor_1)
        []
        """
        events = []
        # Rider can cancel the ride only of the rider is waiting
        if self.rider.status == WAITING:

            # Notify the monitor the Cancellation event
            monitor.notify(self.timestamp, RIDER, CANCEL,
                           self.rider.id, self.rider.origin)
            dispatcher.cancel_ride(self.rider)
        return events


class Pickup(Event):
    """A pickup event let driver pickup rider.

    === Attributes ===
    @type driver: Driver
        A driver.
    @type rider: Rider
        A rider.
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a pickup event.

        @type self: Pickup
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str
        >>> event_1 = Event(7)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> pickup_1 = Pickup(event_1.timestamp, Peter, David)
        >>> str(pickup_1)
        '7 -- David: Pickup Peter'
        """
        return "{} -- {}: Pickup {}".format(self.timestamp, self.driver,
                                            self.rider)

    def do(self, dispatcher, monitor):
        """Change driver's location to rider's location if rider is waiting.

        If rider has cancelled, a new DriverRequestEvent is scheduled.

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> dispatcher_1 = Dispatcher()
        >>> monitor_1 = Monitor()
        >>> event_1 = Event(7)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> John = Rider('John', Location(1,2), Location(3,4), 2)
        >>> dispatcher_1.request_driver(John)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> pickup_1 = Pickup(event_1.timestamp, Peter, David)
        >>> isinstance(pickup_1.do(dispatcher_1, monitor_1)[0], Dropoff)
        True
        >>> dispatcher_1.cancel_ride(Peter)
        >>> isinstance(pickup_1.do(dispatcher_1, monitor_1)[0], DriverRequest)
        True
        """
        events = []
        # Driver drive to the location of the rider
        self.driver.end_drive()
        # Notify the Pickup event for driver
        monitor.notify(self.timestamp, DRIVER, PICKUP,
                       self.driver.id, self.driver.location)

        # If the rider is waiting, the driver will drive the rider to rider's
        # destination
        if self.rider.status == WAITING:

            # Change the status to satisfied when the rider is waiting
            self.rider.status = SATISFIED
            travel_time = self.driver.start_ride(self.rider)
            monitor.notify(self.timestamp, RIDER, PICKUP,
                           self.rider.id, self.rider.origin)
            events.append(Dropoff(self.timestamp + travel_time,
                                  self.rider, self.driver))

        # If the rider has cancelled the ride, the driver will request a new
        # rider, which is appending a new DriverRequest Event
        elif self.rider.status == CANCELLED:
            events.append(
                DriverRequest(self.timestamp, self.driver))

        return events


class Dropoff(Event):
    """A dropoff event let driver dropoff rider.

    === Attributes ===
    @type driver: Driver
        A driver.
    @type rider: Rider
        A rider.
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a dropoff event.

        @type self: Dropoff
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def __str__(self):
        """Return a string representation of this event.

        @type self: Dropoff
        @rtype: str
        >>> event_1 = Event(7)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> dropoff_1 = Dropoff(event_1.timestamp, Peter, David)
        >>> str(dropoff_1)
        '7 -- David: Dropoff Peter'
        """
        return "{} -- {}: Dropoff {}".format(self.timestamp, self.driver,
                                             self.rider)

    def do(self, dispatcher, monitor):
        """Change driver's location to rider's destination and
        leaves the rider satisfied.

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> event_1 = Event(7)
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> dropoff_1 = Dropoff(event_1.timestamp, Peter, David)
        >>> dispatcher_1 = Dispatcher()
        >>> monitor_1 = Monitor()
        >>> isinstance(dropoff_1.do(dispatcher_1, monitor_1)[0], DriverRequest)
        True
        """
        events = []
        # The driver finished the ride
        self.driver.end_ride()
        # Notify the Dropoff event to the monitor for both the driver and the
        # rider
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.id, self.driver.location)
        monitor.notify(self.timestamp, RIDER, DROPOFF,
                       self.rider.id, self.rider.destination)

        # This event lead the driver to request a new rider,
        # which is appending a new DriverRequest Event
        events.append(DriverRequest(self.timestamp, self.driver))
        return events


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):

                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # Append the event when the event is DriverRequest
            if event_type == "DriverRequest":
                identification = tokens[2]
                location = deserialize_location(tokens[3])
                speed = int(tokens[4])
                event = DriverRequest(timestamp, Driver(identification,
                                                        location, speed))
                events.append(event)

            # Append the event when the event is RiderRequest
            elif event_type == "RiderRequest":
                identification = tokens[2]
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                patience = int(tokens[5])
                event = RiderRequest(timestamp, Rider(identification, origin,
                                                      destination, patience))
                events.append(event)
    return events
