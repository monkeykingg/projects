from location import Location, manhattan_distance
"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Rider activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or dropoff.

=== Constants ===
@type RIDER: str
    A constant used for the Rider activity category.
@type DRIVER: str
    A constant used for the Driver activity category.
@type REQUEST: str
    A constant used for the request activity description.
@type CANCEL: str
    A constant used for the cancel activity description.
@type PICKUP: str
    A constant used for the pickup activity description.
@type DROPOFF: str
    A constant used for the dropoff activity description.
"""

RIDER = "rider"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    @type timestamp: int
        The time at which the activity occurred.
    @type description: str
        A description of the activity.
    @type identifier: str
        An identifier for the person doing the activity.
    @type location: Location
        The location at which the activity occurred.
    """

    def __init__(self, timestamp, description, identifier, location):
        """Initialize an Activity.

        @type self: Activity
        @type timestamp: int
        @type description: str
        @type identifier: str
        @type location: Location
        @rtype: None
        """
        self.description = description
        self.time = timestamp
        self.id = identifier
        self.location = location


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    # @type _activities: dict[str, dict[str, list[Activity]]]
    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self):
        """Initialize a Monitor.

        @type self: Monitor
        """
        self._activities = {
            RIDER: {},
            DRIVER: {}
        }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self):
        """Return a string representation.

        @type self: Monitor
        @rtype: str
        >>> a = Monitor()
        >>> a.notify(0, DRIVER, REQUEST, 'David', Location(3,2))
        >>> a.notify(2, RIDER, REQUEST, 'Alice', Location(5,7))
        >>> str(a) == "Monitor (1 drivers, 1 riders)"
        True
        """
        return "Monitor ({} drivers, {} riders)".format(
            len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp, category, description, identifier, location):
        """Notify the monitor of the activity.

        @type self: Monitor
        @type timestamp: int
            The time of the activity.
        @type category: DRIVER | RIDER
            The category for the activity.
        @type description: REQUEST | CANCEL | PICKUP | DROP_OFF
            A description of the activity.
        @type identifier: str
            The identifier for the actor.
        @type location: Location
            The location of the activity.
        @rtype: None
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self):
        """Return a report of the activities that have occurred.

        @type self: Monitor
        @rtype: dict[str, object]
        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self):
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        @type self: Monitor
        @rtype: float
        >>> m1 = Monitor()
        >>> m1.notify(0, DRIVER, REQUEST, 'David', Location(3,2))
        >>> m1.notify(2, RIDER, REQUEST, 'Alice', Location(5,7))
        >>> m1.notify(4, RIDER, CANCEL, 'Alice', Location(5,7))
        >>> m1.notify(5, DRIVER, PICKUP, 'David', Location(5,7))
        >>> m1.notify(5, DRIVER, REQUEST, 'David', Location(5,7))
        >>> m1.report()['rider_wait_time']
        2.0
        >>> m2 = Monitor()
        >>> m2.notify(0, DRIVER, REQUEST, 'Tom', Location(1,1))
        >>> m2.notify(1, RIDER, REQUEST, 'John', Location(2,3))
        >>> m2.notify(2, DRIVER, PICKUP,'Tom', Location(2,3))
        >>> m2.notify(3, DRIVER, REQUEST, 'Jacky', Location(14,16))
        >>> m2.notify(4, DRIVER, DROPOFF,'Tom', Location(4,5))
        >>> m2.notify(4, DRIVER, REQUEST, 'Tom', Location(4,5))
        >>> m2.notify(5, RIDER, REQUEST, 'Ivan', Location(10, 11))
        >>> m2.notify(7, RIDER, CANCEL, 'Ivan', Location(10, 11))
        >>> m2.notify(9, DRIVER, REQUEST, 'Jacky', Location(10, 11))
        >>> m2.report()['rider_wait_time']
        2.0
        """
        wait_time = 0
        count = 0

        for activities in self._activities[RIDER].values():

            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:

                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1

        return wait_time / count

    def _average_total_distance(self):
        """Return the average distance drivers have driven.

        @type self: Monitor
        @rtype: float
        >>> m1 = Monitor()
        >>> m1.notify(0, DRIVER, REQUEST, 'David', Location(3,2))
        >>> m1.notify(2, RIDER, REQUEST, 'Alice', Location(5,7))
        >>> m1.notify(4, RIDER, CANCEL, 'Alice', Location(5,7))
        >>> m1.notify(5, DRIVER, PICKUP, 'David', Location(5,7))
        >>> m1.notify(5, DRIVER, REQUEST, 'David', Location(5,7))
        >>> m1.report()['driver_total_distance']
        7.0
        >>> m2 = Monitor()
        >>> m2.notify(0, DRIVER, REQUEST, 'Tom', Location(1,1))
        >>> m2.notify(1, RIDER, REQUEST, 'John', Location(2,3))
        >>> m2.notify(2, DRIVER, PICKUP,'Tom', Location(2,3))
        >>> m2.notify(3, DRIVER, REQUEST, 'Jacky', Location(14,16))
        >>> m2.notify(4, DRIVER, DROPOFF,'Tom', Location(4,5))
        >>> m2.notify(4, DRIVER, REQUEST, 'Tom', Location(4,5))
        >>> m2.notify(5, RIDER, REQUEST, 'Ivan', Location(10, 11))
        >>> m2.notify(7, RIDER, CANCEL, 'Ivan', Location(10, 11))
        >>> m2.notify(9, DRIVER, REQUEST, 'Jacky', Location(10, 11))
        >>> m2.report()['driver_total_distance']
        8.0
        """
        # Accumulator to get the total distance
        total_distance = 0
        for identifier in self._activities[DRIVER]:

            # Check whether the driver has drove certain amount of distance
            if len(self._activities[DRIVER][identifier]) > 1:

                # Calculate the distance between locations of two nearby
                # activities of the driver and add it to the total distance
                for i in range(1, len(self._activities[DRIVER][identifier])):
                    location1 =\
                        self._activities[DRIVER][identifier][i - 1].location
                    location2 =\
                        self._activities[DRIVER][identifier][i].location
                    total_distance += manhattan_distance(location2, location1)

        # The average of the total distance is the quotient of the total
        # distance and the number of drivers
        return total_distance / len(self._activities[DRIVER])

    def _average_ride_distance(self):
        """Return the average distance drivers have driven on rides.

        @type self: Monitor
        @rtype: float
        >>> m1 = Monitor()
        >>> m1.notify(0, DRIVER, REQUEST, 'David', Location(3,2))
        >>> m1.notify(2, RIDER, REQUEST, 'Alice', Location(5,7))
        >>> m1.notify(4, RIDER, CANCEL, 'Alice', Location(5,7))
        >>> m1.notify(5, DRIVER, PICKUP, 'David', Location(5,7))
        >>> m1.notify(5, DRIVER, REQUEST, 'David', Location(5,7))
        >>> m1.report()['driver_ride_distance']
        0.0
        >>> m2 = Monitor()
        >>> m2.notify(0, DRIVER, REQUEST, 'Tom', Location(1,1))
        >>> m2.notify(1, RIDER, REQUEST, 'John', Location(2,3))
        >>> m2.notify(2, DRIVER, PICKUP,'Tom', Location(2,3))
        >>> m2.notify(3, DRIVER, REQUEST, 'Jacky', Location(14,16))
        >>> m2.notify(4, DRIVER, DROPOFF,'Tom', Location(4,5))
        >>> m2.notify(4, DRIVER, REQUEST, 'Tom', Location(4,5))
        >>> m2.notify(5, RIDER, REQUEST, 'Ivan', Location(10, 11))
        >>> m2.notify(7, RIDER, CANCEL, 'Ivan', Location(10, 11))
        >>> m2.notify(9, DRIVER, REQUEST, 'Jacky', Location(10, 11))
        >>> m2.report()['driver_ride_distance']
        2.0
        """
        # Accumulator
        total_ride_distance = 0

        # Used for getting the location from the Pickup activity
        location = None

        for identifier in self._activities[DRIVER]:

            # Check whether the driver has more than 1 activity
            if len(self._activities[DRIVER][identifier]) > 1:

                # Check the activity for each driver
                for activity in self._activities[DRIVER][identifier]:

                    # Get the location if the location is Pickup
                    if activity.description == PICKUP:
                        location = activity.location

                    # Calculate the distance by the Dropoff location and
                    # the Pickup location.
                    if activity.description == DROPOFF:
                        total_ride_distance += \
                            manhattan_distance(activity.location, location)

        # The average of the total ride distance is the quotient of the total
        # distance and the number of drivers
        return total_ride_distance / len(self._activities[DRIVER])
