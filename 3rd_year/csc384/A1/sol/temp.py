def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    se = SearchEngine('custom', 'full')

    se.init_search(initial_state, goal_fn=snowman_goal_state, heur_fn=heur_fn,
                   fval_function=(lambda sN: fval_function(sN, weight=weight)))

    initial_time = os.times()[0]
    remainning_time = timebound

    cost_bound = (float("inf"), float("inf"), float("inf"))

    current_state = se.search(timebound, cost_bound)

    if current_state == False:
        return False

    best_gval = current_state.gval

    if current_state != False:
        while remainning_time > 0:

            current_time = os.times()[0]
            passed_time = current_time - initial_time
            remainning_time = remainning_time - passed_time
            initial_time = current_time

            if best_gval < cost_bound[2]:
                new_cost_bound = (float("inf"), float("inf"), best_gval)
            else:
                new_cost_bound = cost_bound

            new_state = se.search(remainning_time, new_cost_bound)

            if new_state == False:
                return current_state
            else:
                new_gval = new_state.gval
                if new_gval < best_gval:
                    current_state = new_state
                    best_gval = new_gval
    return current_state


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    se = SearchEngine('custom', 'full')

    se.init_search(initial_state, goal_fn=snowman_goal_state, heur_fn=heur_fn,
                   fval_function=(lambda sN: fval_function(sN, weight=weight)))

    current_time = os.times()[0]

    cost_bound = (float('inf'), float('inf'), float('inf'))

    states = [None]

    while timebound > 0:

        current_state = se.search(timebound, cost_bound)

        if current_state:

            if current_state.gval < cost_bound[2]:

                cost_bound = (float('inf'), float('inf'), current_state.gval)

                states.pop()
                states.append(current_state)

        passed_time = os.times()[0] - current_time
        timebound = timebound - passed_time
        current_time = os.times()[0]

    if states[0] is None:
        return False

    return states[0]

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

    # build a dictionary to store the UP, LEFT, RIGHT, DOWN side coordinates of
    # all snowballs/snowman
    around_snowball = {}
    for key in state.snowballs:
        around_snowball[key] = []

        # UP side, index = 0
        around_snowball[key].append((key[0], key[1] - 1))

        # LEFT side, index = 1
        around_snowball[key].append((key[0] - 1, key[1]))

        # RIGHT side, index = 2
        around_snowball[key].append((key[0] + 1, key[1]))

        # DOWN side, index = 3
        around_snowball[key].append((key[0], key[1] + 1))

        # add snowballs coordinates to the list
        snowballs.append(key)

    obstacles = set()

    for item in state.obstacles:
        obstacles.add(item)
    for x in range(0, state.width):
        obstacles.add((x, -1))
        obstacles.add((x, state.height))
    for y in range(0, state.height):
        obstacles.add((-1, y))
        obstacles.add((state.width, y))

    # build a list to store the edges that destination stick to
    d_edges = []

    # destination stick at North edge
    if state.destination[1] == 0:
        d_edges.append('N')
    # destination stick at West edge
    if state.destination[0] == 0:
        d_edges.append('W')
    # destination stick at East edge
    if state.destination[0] == state.width:
        d_edges.append('E')
    # destination stick at South edge
    if state.destination[1] == state.height:
        d_edges.append('S')

    # build a list to store the edges that current snowball stick to
    s_edges = []

    # check all snowballs' edges
    for snowball in snowballs:

        # snowball stick at North edge
        if snowball[1] == 0:
            s_edges.append('N')
        # snowball stick at West edge
        if snowball[0] == 0:
            s_edges.append('W')
        # snowball stick at East edge
        if snowball[0] == state.width:
            s_edges.append('E')
        # snowball stick at South edge
        if snowball[1] == state.height:
            s_edges.append('S')

    # if any snowball stick at any edge
    if len(s_edges) > 0:

        # if destination is not at any edge
        if len(d_edges) == 0:
            distance += float("inf")

        # if destination is at any edge
        else:

            # set a flag to check if destination and snowballs can share the
            # same edge
            flag = False

            # go over all edges that destination stick to
            for edge in d_edges:

                # if destination and snowballs can share the same edge
                # then we are able to get solution at this case
                # there are more checkings below
                if edge in s_edges:
                    flag = True

            # if destination and snowballs cannot share the same edge
            if flag == False:
                distance += float("inf")

    # get total number of snowballs and snowman
    total = len(snowballs)

    # if there are 3 snowballs on the stage
    if total == 3:

        # set a flag to check if current snowball already at destination
        flag = False

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
            if state.snowballs[snowball] == 1:
                medium = snowball

                # if big snowball already at the destination
                if flag:
                    distance += abs(robot_position[0] - medium[0]) + \
                                abs(robot_position[1] - medium[1]) - 1

            # check if current snowball at corner
            corners = 0
            # UP and LEFT
            if (around_snowball[snowball][0] in state.obstacles) and \
               (around_snowball[snowball][1] in state.obstacles):
                corners += 1
            # UP and RIGHT
            if (around_snowball[snowball][0] in state.obstacles) and \
               (around_snowball[snowball][2] in state.obstacles):
                corners += 1
            # DOWN and LEFT
            if (around_snowball[snowball][3] in state.obstacles) and \
               (around_snowball[snowball][1] in state.obstacles):
                corners += 1
            # DOWN and RIGHT
            if (around_snowball[snowball][3] in state.obstacles) and \
               (around_snowball[snowball][2] in state.obstacles):
                corners += 1

            # if current snowball at corner
            if corners > 0:

                # if current snowball is not big snowball and not at desination
                if (flag == False) and (state.snowballs[snowball] != 0):
                    distance += float("inf")

    # if there are 1 snowball and 1 snowman on the stage
    if total == 2:

        # A flag to check if big snowball already at destination
        flag = False

        for snowball in snowballs:

            if state.snowballs[snowball] == 2:
                distance += abs(robot_position[0] - snowball[0]) + \
                            abs(robot_position[1] - snowball[1]) - 1

            if state.snowballs[snowball] in [0, 1, 4, 5]:
                distance += float("inf")

            if state.snowballs[snowball] == 3:
                m_on_b = snowball
                if m_on_b != state.destination:
                    distance += float("inf")
                else:
                    flag = True

            corners = 0
            # UP and LEFT
            if (around_snowball[snowball][0] in state.obstacles) and \
               (around_snowball[snowball][1] in state.obstacles):
                corners += 1
            # UP and RIGHT
            if (around_snowball[snowball][0] in state.obstacles) and \
               (around_snowball[snowball][2] in state.obstacles):
                corners += 1
            # DOWN and LEFT
            if (around_snowball[snowball][3] in state.obstacles) and \
               (around_snowball[snowball][1] in state.obstacles):
                corners += 1
            # DOWN and RIGHT
            if (around_snowball[snowball][3] in state.obstacles) and \
               (around_snowball[snowball][2] in state.obstacles):
                corners += 1

            if corners > 0:
                if flag == False:
                    distance += float("inf")

        # if there are 1 snowman on the stage
        if total == 1:

            for snowball in state.snowballs:
                if state.snowballs[snowball] == 0:
                    distance = abs(state.destination[0] - key[0]) + \
                               abs(state.destination[1] - key[1])
                    if distance != 0:
                        distance += float("inf")

    return distance
