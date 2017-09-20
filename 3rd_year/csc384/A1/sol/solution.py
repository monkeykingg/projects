#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Snowman Puzzle domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes and problems
from test_problems import PROBLEMS #20 test problems

#snowball HEURISTICS
def heur_simple(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  return len(state.snowballs)

def heur_zero(state):
  return 0

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible snowball puzzle heuristic: manhattan distance'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between the snowballs and the destination for the Snowman is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    # init a result for future calculation
    result = 0

    # loop over all snowballs
    for key in state.snowballs:

        # if at key coordinate, there is a snowman formed by 2 snowballs
        if state.snowballs[key] in [3, 4, 5]:
            result += (abs(state.destination[0] - key[0]) + \
                       abs(state.destination[1] - key[1])) * 2
            break

        # if at key coordinate, there is a snowman formed by 3 snowballs
        if state.snowballs[key] == 6:
            result += (abs(state.destination[0] - key[0]) + \
                       abs(state.destination[1] - key[1])) * 3
            break

        # if at key coordinate, there is only one snowball
        result += abs(state.destination[0] - key[0]) + \
                  abs(state.destination[1] - key[1])

    return result

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    # init the distance of all snowballs to destination.
    distance = heur_manhattan_distance(state)

    # init a list to store all coordinates of snowballs
    snowballs = []

    # get the position of robot
    robot_position = state.robot

    for key in state.snowballs:

        # add snowballs coordinates to the list
        snowballs.append(key)

    # build a set to store obstacles, including the edges of the stage
    obstacles = set()

    # add original obstacles
    for item in state.obstacles:
        obstacles.add(item)

    # add UP and DOWN edge
    for x in range(0, state.width):
        obstacles.add((x, -1))
        obstacles.add((x, state.height))

    # add LEFT and RIGHT edge
    for y in range(0, state.height):
        obstacles.add((-1, y))
        obstacles.add((state.width, y))

    # get total number of snowballs and snowman
    total = len(snowballs)

    # if there are 3 snowballs on the stage
    # we should move big snowball first
    if total == 3:

        # set a flag to check if current snowball already at destination
        flag = False

        medium = (0, 0)

        for snowball in snowballs:

            # if the current snowball is the big snowball
            if state.snowballs[snowball] == 0:
                big = snowball

                # if the current big snowball is not at destination,
                # then we should move this snowball first
                if big != state.destination:
                    distance += abs(robot_position[0] - big[0]) + \
                                abs(robot_position[1] - big[1]) - 1
                else:
                    flag = True

            # if the current snowball is the medium snowball
            elif state.snowballs[snowball] == 1:
                medium = snowball

            # check if current snowball at corner
            corners = 0
            # UP and LEFT
            if ((snowball[0], snowball[1] - 1) in obstacles) and \
               ((snowball[0] - 1, snowball[1]) in obstacles):
                corners += 1
            # UP and RIGHT
            if ((snowball[0], snowball[1] - 1) in obstacles) and \
               ((snowball[0] + 1, snowball[1]) in obstacles):
                corners += 1
            # DOWN and LEFT
            if ((snowball[0], snowball[1] + 1) in obstacles) and \
               ((snowball[0] - 1, snowball[1]) in obstacles):
                corners += 1
            # DOWN and RIGHT
            if ((snowball[0], snowball[1] + 1) in obstacles) and \
               ((snowball[0] + 1, snowball[1]) in obstacles):
                corners += 1

            # if current snowball at corner
            if corners > 0:

                # if current snowball is not big snowball and not at desination
                if (flag == False) or (state.snowballs[snowball] != 0):
                    distance += float("inf")

        # if big snowball already at the destination
        if flag:
            distance += abs(robot_position[0] - medium[0]) + \
                        abs(robot_position[1] - medium[1]) - 1

    # if there are 1 snowball and 1 snowman on the stage
    # we should move small ball first because we assume medium snowball
    # atop big snowball and they already at the destination
    if total == 2:

        for snowball in snowballs:

            # if current snowball is not small snowball nor medium snowball
            # atop big snowball
            if state.snowballs[snowball] in [4, 5]:
                distance += float("inf")

            # if current snowball is medium snowball atop big snowball
            elif state.snowballs[snowball] == 3:
                m_on_b = snowball

                # if medium snowball atop big snowball are not at destination
                if m_on_b != state.destination:
                    distance += float("inf")
                else:

                    copy_list = snowballs.copy()
                    copy_list.remove(snowball)
                    snowball = copy_list[0]

                    # check if current snowball at corner
                    corners = 0
                    # UP and LEFT
                    if ((snowball[0], snowball[1] - 1) in obstacles) and \
                            ((snowball[0] - 1, snowball[1]) in obstacles):
                        corners += 1
                    # UP and RIGHT
                    if ((snowball[0], snowball[1] - 1) in obstacles) and \
                            ((snowball[0] + 1, snowball[1]) in obstacles):
                        corners += 1
                    # DOWN and LEFT
                    if ((snowball[0], snowball[1] + 1) in obstacles) and \
                            ((snowball[0] - 1, snowball[1]) in obstacles):
                        corners += 1
                    # DOWN and RIGHT
                    if ((snowball[0], snowball[1] + 1) in obstacles) and \
                            ((snowball[0] + 1, snowball[1]) in obstacles):
                        corners += 1

                    if corners > 0:
                        distance += float("inf")
                    else:
                        distance += abs(robot_position[0] - snowball[0]) + \
                                    abs(robot_position[1] - snowball[1]) - 1

    return distance

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SnowballState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    return sN.gval + weight * sN.hval

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    # init basic settings
    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, goal_fn=snowman_goal_state, heur_fn=heur_fn)

    # time control
    initial_time = os.times()[0]
    remainning_time = timebound

    # init cost bound for future update
    cost_bound = (float("inf"), float("inf"), float("inf"))

    # get current state for future update
    current_state = se.search(timebound, cost_bound)

    # error checking
    if current_state == False:
        return False

    # get g value for future comparison and update
    best_gval = current_state.gval

    if current_state != False:

        # time checking
        while remainning_time > 0:

            # time updating
            current_time = os.times()[0]
            passed_time = current_time - initial_time
            remainning_time = remainning_time - passed_time
            initial_time = current_time

            # g value comparison and cost bound update
            if best_gval < cost_bound[0]:
                new_cost_bound = (best_gval, float("inf"), float("inf"))
            else:
                new_cost_bound = cost_bound

            # get new state
            new_state = se.search(remainning_time, new_cost_bound)

            # error checking
            if new_state == False:
                return current_state

            # update current state and g value based on g value comparison
            else:
                if new_state.gval < best_gval:
                    current_state = new_state
                    best_gval = new_state.gval

    return current_state

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    # init basic settings
    se = SearchEngine('custom', 'full')
    se.init_search(initial_state, goal_fn=snowman_goal_state, heur_fn=heur_fn,
                   fval_function=(lambda sN: fval_function(sN, weight=weight)))

    # time control
    initial_time = os.times()[0]
    remainning_time = timebound

    # init cost bound for future update
    cost_bound = (float("inf"), float("inf"), float("inf"))

    # get current state for future update
    current_state = se.search(timebound, cost_bound)

    # error checking
    if current_state == False:
        return False

    # get g value for future comparison and update
    best_gval = current_state.gval

    if current_state != False:

        # time checking
        while remainning_time > 0:

            # time updating
            current_time = os.times()[0]
            passed_time = current_time - initial_time
            remainning_time = remainning_time - passed_time
            initial_time = current_time

            # g value comparison and cost bound update
            if best_gval < cost_bound[2]:
                new_cost_bound = (float("inf"), float("inf"), best_gval)
            else:
                new_cost_bound = cost_bound

            # get new state
            new_state = se.search(remainning_time, new_cost_bound)

            # error checking
            if new_state == False:
                return current_state

            # update current state and g value based on g value comparison
            else:
                if new_state.gval < best_gval:
                    current_state = new_state
                    best_gval = new_state.gval

    return current_state

if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")
  print("Running A-star")

  for i in range(0, 10): #note that there are 20 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=snowman_goal_state, heur_fn=heur_simple)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit
  print("Running Anytime Weighted A-star")

  for i in range(0, 10):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_simple, weight=weight, timebound=timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")


