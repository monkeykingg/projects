"""Snowball routines.

    A) Class SnowmanState

    A specializion of the StateSpace Class that is tailored to the game of Snowball.

    B) class Direction

    An encoding of the directions of movement that are possible for robots in Snowball.

    Code also contains a list of 40 Snowball problems for the purpose of testing.
"""

from search import *

class SnowmanState(StateSpace):

    def __init__(self, action, gval, parent, width, height, robot, snowballs, obstacles, destination):
        """
        Create a new Snowman state.

        @param width: The yard's X dimension (excluding walls).
        @param height: The yard's Y dimension (excluding walls).
        @param robot: A tuple of the robot's location.
        @param snowballs: A dictionary where the keys are the coordinates of each snowball, and the values are the index of that snowball's size.
        @param obstacles: A frozenset of all the impassable obstacles.
        @param snowball_sizes: A mapping from each snowball to the size of the snowball.
        """
        StateSpace.__init__(self, action, gval, parent)
        self.width = width
        self.height = height
        self.robot = robot
        self.destination = destination        
        self.snowballs = snowballs
        self.obstacles = obstacles
        
        #snowball sizes: 'b' is 'big', 'm' is 'medium' and 's' is small.  'G' is a complete snowman.
        #A type 'A' snowman is formed by placing a medium snowball atop big one.
        #A type 'B' snowman is formed by placing a small snowball atop a medium one.
        #A type 'C' snowman is formed by placing a small snowball atop a big one.
        self.snowball_sizes = {0: 'b', 1: 'm', 2: 's', 3: 'A', 4: 'B', 5: 'C', 6: 'G'} 


    def successors(self):
        """
        Generate all the actions that can be performed from this state, and the states those actions will create.        
        """
        successors = []
        transition_cost = 1

        for direction in (UP, RIGHT, DOWN, LEFT):

            new_location = direction.move(self.robot)
            
            if new_location[0] < 0 or new_location[0] >= self.width:
                continue
            if new_location[1] < 0 or new_location[1] >= self.height:
                continue
            if new_location in self.obstacles:
                continue
            
            new_snowballs = dict(self.snowballs)
            index = 0

            if new_location in self.snowballs:
                new_snowball_location = direction.move(new_location)
                
                if new_snowball_location[0] < 0 or new_snowball_location[0] >= self.width:
                    continue
                if new_snowball_location[1] < 0 or new_snowball_location[1] >= self.height:
                    continue
                if new_snowball_location in self.obstacles:
                    continue        
                if self.snowball_sizes[new_snowballs[new_location]] == 'G': #can't move a complete Snowman       
                    continue  

                #cases where bigger snowball is pushed atop smaller one(s)        
                if new_snowball_location in new_snowballs:
                    if self.snowball_sizes[new_snowballs[new_snowball_location]] == 'b' and self.snowball_sizes[new_snowballs[new_location]] == 'm':
                        index = 3 #will transition to A formation of snowballs
                    elif self.snowball_sizes[new_snowballs[new_snowball_location]] == 'm' and self.snowball_sizes[new_snowballs[new_location]] == 's':
                        index = 4 #will transition to B formation of snowballs
                    elif self.snowball_sizes[new_snowballs[new_snowball_location]] == 'b' and self.snowball_sizes[new_snowballs[new_location]] == 's':
                        index = 5  #will transition to C formation of snowballs 
                    elif self.snowball_sizes[new_snowballs[new_snowball_location]] == 'A' and self.snowball_sizes[new_snowballs[new_location]] == 's':
                        index = 6  #will transition to Goal formation of snowballs               
                    else:
                        continue

                #cases where a stack of snowballs is pushed apart                             
                if self.snowball_sizes[new_snowballs[new_location]] == 'A':
                    new_snowballs[new_location] = 0 #b
                    new_snowballs[new_snowball_location] = 1 #m  
                    index = 7;                 
                if self.snowball_sizes[new_snowballs[new_location]] == 'B':
                    new_snowballs[new_location] = 1 #m
                    new_snowballs[new_snowball_location] = 2 #s     
                    index = 7;   
                if self.snowball_sizes[new_snowballs[new_location]] == 'C':
                    new_snowballs[new_location] = 0 #b
                    new_snowballs[new_snowball_location] = 2 #s 
                    index = 7;               

                if index == 0: #case robot has pushed one snowball
                    index = new_snowballs.pop(new_location)
                elif index != 7: #case robot has pushed snowballs stack apart          
                    new_snowballs.pop(new_location)
                    new_snowballs.pop(new_snowball_location)
                
                if index < 7: #case robot has pushed two snowballs together
                    new_snowballs[new_snowball_location] = index
            
            if index == 7: #if robot pushed snowball stack apart, no movement of robot results
                new_robot = self.robot
            else:
                new_robot = tuple(new_location)

            new_state = SnowmanState(action=direction.name, gval=self.gval + transition_cost, parent=self,
                                     width=self.width, height=self.height, robot=new_robot,
                                     snowballs=new_snowballs, obstacles=self.obstacles, destination=self.destination)
            successors.append(new_state)

        return successors

    def hashable_state(self):
        """
        Return a data item that can be used as a dictionary key to UNIQUELY represent a state.
        """
        return hash((self.robot, frozenset(self.snowballs.items())))


    def state_string(self):
        """
        Return a string representation of a state that can be printed to stdout.

        """
        map = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row += [' ']
            map += [row]

        if self.robot in self.obstacles:
            print("error: robot is in list of obstacles")

        if self.destination in self.obstacles:
            print("error: destination for snowman is in list of obstacles")

        for obstacle in self.obstacles:
            map[obstacle[1]][obstacle[0]] = '#'

        map[self.destination[1]][self.destination[0]] = 'X'

        for snowball in self.snowballs:
            map[snowball[1]][snowball[0]] = self.snowball_sizes[self.snowballs[snowball]]
            if snowball in self.obstacles:
                print("error: snowball is in list of obstacles")

        map[self.robot[1]][self.robot[0]] = '?'

        for y in range(0, self.height):
            map[y] = ['#'] + map[y]
            map[y] = map[y] + ['#']
        map = ['#' * (self.width + 2)] + map
        map = map + ['#' * (self.width + 2)]        

        s = ''
        for row in map:
            for char in row:
                s += char
            s += '\n'

        return s   


    def print_state(self):
        """
        Print the string representation of the state. ASCII art FTW!
        """        
        print("ACTION was " + self.action)      
        print(self.state_string())


def removekey(d, key):    
    r = dict(d)
    del r[key]
    return r

def snowman_goal_state(state):
  """
  Returns True if we have reached a goal state.

  @param state: a Snowball state
  OUTPUT: True (if goal) or False (if not)
  """
  for snowball in state.snowballs:
    if(state.snowball_sizes[state.snowballs[snowball]] == 'G' and snowball[1] == state.destination[1] and snowball[0] == state.destination[0]): #means a complete snowman is on the board and in the right spot
        return True
  return False 

def generate_coordinate_rect(x_start, x_finish, y_start, y_finish):
    """
    Generate tuples for coordinates in rectangle (x_start, x_finish) -> (y_start, y_finish)
    """
    coords = []
    for i in range(x_start, x_finish):
        for j in range(y_start, y_finish):
            coords.append((i, j))
    return coords

"""
Snowball Directions: encodes directions of movement that are possible for each robot.
"""
class Direction():
    """
    A direction of movement.
    """
    
    def __init__(self, name, delta):
        """
        Creates a new direction.
        @param name: The direction's name.
        @param delta: The coordinate modification needed for moving in the specified direction.
        """
        self.name = name
        self.delta = delta
    
    def __hash__(self):
        """
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        """
        return hash(self.name)
    
    def __str__(self):
        """
        @return: The string representation of this object when *str* is called.
        """
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()
    
    def move(self, location):
        """
        @return: Moving from the given location in this direction will result in the returned location.
        """
        return (location[0] + self.delta[0], location[1] + self.delta[1])


#Global Directions
UP = Direction("up", (0, -1))
RIGHT = Direction("right", (1, 0))
DOWN = Direction("down", (0, 1))
LEFT = Direction("left", (-1, 0))



  
