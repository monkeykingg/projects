from driver import Driver
from rider import Rider, CANCELLED
from location import Location


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        self._wait_list = []
        self._driver_list = []

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """
        return "Waiting Riders:{}".format(self._wait_list)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> James = Rider('James', Location(4,9), Location(3,6), 3)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> dispatcher1 = Dispatcher()
        >>> dispatcher1.request_driver(Peter)
        >>> dispatcher1.request_rider(David).id
        'Peter'
        >>> dispatcher1.request_driver(James) is None
        True
        """
        # Accumulator for getting the drivers who are idle
        available_drivers = []

        # Accumulate the available drivers
        for driver in self._driver_list:
            if driver.is_idle:
                available_drivers.append(driver)

        # If there is no available driver, add the rider to the waitlist
        if len(available_drivers) == 0:
            self._wait_list.append(rider)

        # If there are drivers available, get the driver who can take the
        # least time to pick up the driver.
        else:
            closest = available_drivers[0]
            for driver in available_drivers:
                time1 = driver.get_travel_time(rider.origin)
                time2 = closest.get_travel_time(rider.origin)
                if time1 < time2:
                    closest = driver
            return closest

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> David = Driver('David', Location(5, 3), 2)
        >>> dispatcher1 = Dispatcher()
        >>> dispatcher1.request_driver(Peter)
        >>> dispatcher1.request_rider(David).id
        'Peter'
        >>> dispatcher1.request_rider(David)
        """
        # If the driver is not in the driver list, register the new driver.
        if driver not in self._driver_list:
            self._driver_list.append(driver)

        # Driver requests the rider who wait most of time in the waitlist
        if len(self._wait_list) != 0:

            # Get the rider who wait the most of the time
            rider = self._wait_list.pop(0)
            driver.start_drive(rider.origin)
            return rider

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        >>> Peter = Rider('Peter', Location(2,4), Location(3,6), 2)
        >>> dispatcher1 = Dispatcher()
        >>> dispatcher1.cancel_ride(Peter)
        >>> Peter.status
        'cancelled'
        """
        # Change the status to cancel
        rider.status = CANCELLED

        # Remove the rider from waitlist if the rider is in the waitlist
        if rider in self._wait_list:
            self._wait_list.remove(rider)
