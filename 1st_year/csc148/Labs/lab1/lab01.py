class Race:
    """A system for organizing a 5K running race.
    
    assume the name is the email address    
    
    Attributes:
    ===========
    @type runners_speed: dict of {str:int}
          every runner and his/her max speed
    @type speed_of_runners: dict of {int:list of str}
          runners who under this speed
    """
    def __init__(self):
        """init attributes
        
        @type self: Race
        @rtype: none
        
        >>>system = Race()
        >>>print(system.runners_speed)
        {}
        >>>print(system.speed_of_runners)
        {}
        """
        self.runners_speed = {}
        self.speed_of_runners = {}
        
    def __eq__(self, other):
        """check if system is the same
        
        @type self: Race
        @type other: Race
        @rtype: bool
        
        >>>system1 = Race()
        >>>system2 = Race()
        >>>system1.add_runner("Tom", 30)
        >>>system2.add_runner("Toni", 20)
        >>>return(system1 == system2)
        False
        """
        if system1 != system2:
            return False
        else:
            return True
        
    def __str__(self):
        """return string of race
        
        @type self: Race
        @rtype: str
        
        >>>system = Race()
        >>>system.add_runner("Tom", 30)
        >>>print(system)
        """
        result = ""
        for speed in self.speed_of_runners:
            result += "{},with time under,{},minutes".format(self.speed_of_runners, speed)
            
    def add_runner(self, runner, speed):
        """add runner and speed into system
    
        @type self: Race
        @type runner: str
        @type speed: int
        @rtype: none
        
        >>>system = Race()
        >>>system.add_runner("Tom", 30)
        """
        if speed not in self.speed_of_runners:
            self.speed_of_runners[speed] = [runner]
        else:
            self.speed_of_runners[speed].append(runner)
        self.runners_speed[runner] = speed
            
    def get_runners_by_speed(self, speed):
        """return runners
        
        @type self: Race
        @type speed: int
        @rtype: list
        """
        return self.speed_of_runners[speed]
        
    def get_speed_by_runner(self, runner):
        """return speed
        
        @type self: Race
        @type runner: str
        @rtype: int
        """
        return self.runners_speed[runner]