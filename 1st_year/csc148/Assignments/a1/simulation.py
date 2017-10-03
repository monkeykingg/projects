from container import PriorityQueue
from dispatcher import Dispatcher
from event import create_event_list, Event, DriverRequest, RiderRequest
from monitor import Monitor
from driver import Driver
from rider import Rider
from location import Location


class Simulation:
    """A simulation.

    This is the class which is responsible for setting up and running a
    simulation.

    The API is given to you: your main task is to implement the run
    method below according to its docstring.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """

    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _dispatcher: Dispatcher
    #     The dispatcher associated with the simulation.
    # @type _monitor: monitor
    #     The monitor which is used to record the events

    def __init__(self):
        """Initialize a Simulation.

        @type self: Simulation
        @rtype: None
        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events):
        """Run the simulation on the list of events in <initial_events>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @type self: Simulation
        @type initial_events: list[Event]
            An initial list of events.
        @rtype: dict[str, object]
        >>> event_list_1 = [RiderRequest(1, Rider('Z', Location(1,1),\
        Location(6,6), 15)), ]
        >>> event_list_1.append(DriverRequest(10, Driver('Y',\
         Location(3,3), 2)))
        >>> simulation_1 = Simulation()
        >>> d1 = simulation_1.run(event_list_1)
        >>> d2 = {'rider_wait_time': 11.0, 'driver_ride_distance': 10.0,\
        'driver_total_distance': 14.0}
        >>> d1 == d2
        True
        >>> event_list_2 = [DriverRequest(0, Driver('A', Location(1,1), 1)), \
        DriverRequest(0, Driver('B', Location(1,2), 1)),RiderRequest(0, \
        Rider('A2', Location(1,1),Location(5,5), 10)), RiderRequest(10,\
        Rider('B2', Location(4,2), Location(1,5), 15)) ]
        >>> simulation_2 = Simulation()
        >>> d3 = simulation_2.run(event_list_2)
        >>> d4 = {'driver_ride_distance': 7.0, 'driver_total_distance': 8.5,\
        'rider_wait_time': 1.5}
        >>> d3 == d4
        True
        """

        # Add all initial events to the event queue.
        for event in initial_events:
            self._events.add(event)

        while not self._events.is_empty():

            # Get the most nearest event, and remove it from the event queue
            removed_event = self._events.remove()

            # Do the event
            if isinstance(removed_event, Event):
                new_events = removed_event.do(self._dispatcher, self._monitor)

                # Append the result events back
                for event in new_events:
                    self._events.add(event)

        return self._monitor.report()

if __name__ == "__main__":
    events = create_event_list("events.txt")
    sim = Simulation()
    final_stats = sim.run(events)
    print(final_stats)
