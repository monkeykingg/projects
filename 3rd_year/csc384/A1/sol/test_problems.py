"""20 Snowman test problems.
"""
from snowman import SnowmanState

def generate_coordinate_rect(x_start, x_finish, y_start, y_finish):
    """
    Generate tuples for coordinates in rectangle (x_start, x_finish) -> (y_start, y_finish)
    """
    coords = []
    for i in range(x_start, x_finish):
        for j in range(y_start, y_finish):
            coords.append((i, j))
    return coords


PROBLEMS = (
    #Problem 0,
    SnowmanState("START", 0, None, 4, 4, # dimensions
                 (0, 3), #robot
                 {(1, 2): 0, (1, 1): 1, (2, 1): 2}, #snowballs
                 frozenset(((0, 0), (3, 3))), #obstacles
                 (1, 3), #destination                 
                 ),
    # Problem 1,
    SnowmanState("START", 0, None, 5, 4, # dimensions
             (0, 3), #robot
             {(2, 2): 0, (3, 1): 1, (1, 2): 2}, #snowballs
             frozenset(((0, 0), (4, 0), (2, 3), (3, 3), (4, 3))), #obstacles
             (3, 2), #destination                 
             ),    
    # Problem 2,
    SnowmanState("START", 0, None, 6, 4, # dimensions
             (5, 3), #robot
             {(2, 1): 0, (3, 1): 1, (3, 2): 2}, #snowballs
             frozenset(((0, 0), (5, 0), (0, 3), (1, 3), (2, 3), (3, 3))), #
             (2, 2), #destination                     
             ),
    # Problem 3
    SnowmanState("START", 0, None, 5, 5, # dimensions
                 (2, 1), # robot
                 {(2, 3): 0, (1, 2): 1, (3, 2): 2}, #snowballs
                 frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4))), #obstacles
                 (4, 4), #destination                       
                 ),
    # Problem 4
    SnowmanState("START", 0, None, 6, 6, # dimensions
                 (4, 0), #robot
                 {(3, 1): 0, (3, 2): 1, (3, 3): 2}, #snowballs
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))), #obstacles
                 (2, 2), #destination                       
                 ),
    # Problem 5, 
    SnowmanState("START", 0, None, 7, 7, # dimensions
                 (4, 0), #robot
                 {(3, 1): 0, (3, 2): 1, (1, 3): 2}, #snowballs
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4), (2, 5))), #obstacles
                 (2, 2), #destination                      
                 ),
    # Problem 6,
    SnowmanState("Start", 0, None, 6, 7, # dimensions
        (5, 5), #robot
        {(3, 3): 0, (3, 4): 1, (3, 5): 2}, # snowballs
        frozenset(((1, 2), (1, 3), (1, 4), (1, 5),(1, 6), (2, 2), (5, 1), (5, 0))), # obstacles
        (2, 3), #destination              
        ),    
    # Problem 7, 
    SnowmanState("Start", 0, None, 6, 4, # dimensions
        (2, 2),
        {(1, 1): 0, (2, 1): 1, (4, 1): 2}, # snowballs
        frozenset(((0, 0), (2, 0), (3, 0), (0, 3), (1, 3), (2, 3))), # obstacles
        (1, 0), #destination             
        ),
    # Problem 8,
    SnowmanState("Start", 0, None, 6, 7, # dimensions
        (1, 0), # robot
        {(2, 1): 0, (1, 4): 1, (4, 5): 2}, # snowballs
        frozenset(((0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (3, 2), (3, 3), (4, 4),
        (3, 0), (4, 0), (5, 0), (5, 1), (5, 2))), # obstacles
        (2, 2), #destination             
        ),
    #Problem 9,
    SnowmanState("START", 0, None, 6, 4, # dimensions
         (4, 3), #robot
         {(3, 1): 0, (3, 2): 2, (4, 2): 1}, #snowballs
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                   + generate_coordinate_rect(0, 3, 3, 4))), #obstacles
         (3, 3), #destination
         ),   

    #Problem 10
    SnowmanState("START", 0, None, 6, 4, # dimensions
         (5, 2), #robot
         {(3, 1): 0, (2, 2): 1, (3, 2): 2}, #snowballs
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                   + generate_coordinate_rect(0, 3, 3, 4))), #obstacles
         (5, 1), #destination
         ),
    #Problem 11 
    SnowmanState("START", 0, None, 6, 5, # dimensions
         (5, 2), #robot
         {(3, 1): 0, (3, 2): 1, (3, 3): 2}, #snowballs
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                    + generate_coordinate_rect(3, 6, 4, 5))
                    + [(1, 1), (1, 3)]), #obstacles
         (5, 1), #destination
         ),  
    # Problem 12
    SnowmanState("START", 0, None, 6, 4, # dimensions
         (5, 3), #robot
         {(3, 1): 0, (2, 2): 1, (3, 2): 2}, #snowballs
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                   + generate_coordinate_rect(0, 3, 3, 4))), #obstacles
         (2, 1), #destination          
         ),

    #Problem 13 
    SnowmanState("START", 0, None, 8, 6, # dimensions
         (1, 2), #robot
         {(1, 3): 0, (2, 3): 1, (3, 3): 2}, #snowballs
         frozenset((generate_coordinate_rect(0, 7, 0, 2) + [(0, 2), (6, 2), (7, 5)]
         + generate_coordinate_rect(0, 5, 5, 6))), #obstacles
         (7, 0), #destination
         ),

    # Problem 14
    SnowmanState("START", 0, None, 8, 8, # dimensions
        (0, 5), #robot
        {(1, 5): 0, (3, 5): 1, (4, 5): 2}, # snowballs
        frozenset(((0, 4), (1, 4), (2, 4), (3, 4))), # obstacles
        (0, 2), #destination             
        ),

    # Problem 15
    SnowmanState("Start", 0, None, 8, 7, # dimensions
        (5, 5), # robot
        {(1, 3): 1, (3, 2): 0, (2, 1): 2}, # snowballs
        frozenset(((0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (1, 5), (1, 6), (7, 6), (7, 5),
        (7, 4), (7, 3), (7, 2), (2, 2), (4, 2), (5, 2), (5, 1))), # obstacles
        (2, 3), #destination             
        ),    

    # Problem 16
    SnowmanState("START", 0, None, 9, 6, # dimensions
        (0, 0), #robot
        {(2, 1): 0, (6, 4): 1, (6, 3): 2}, # snowballs
        frozenset((generate_coordinate_rect(2, 7, 2, 3) + generate_coordinate_rect(2, 3, 2, 6))), # obstacles
        (2, 0), #destination              
        ),
    # Problem 17
    SnowmanState("START", 0, None, 10, 7, # dimensions
        (0, 0), #robot
        {(5, 3): 0, (7, 4): 1, (7, 5): 2}, # snowballs
        frozenset((generate_coordinate_rect(2, 8, 2, 3) + generate_coordinate_rect(2, 3, 2, 7))), # obstacles
        (2, 0), #destination              
        ),

    # Problem 18
    SnowmanState("Start", 0, None, 6, 5, # dimensions
        (1, 4), # robot
        {(2, 2): 0, (1, 2): 1, (4, 1): 2}, # snowballs
        frozenset(((1, 3), (0, 3))), # obstacles
        (0, 4), #destination              
        ),
    # Problem 19
    SnowmanState("Start", 0, None, 7, 6, # dimensions
        (1, 0),
        {(1, 1): 0, (2, 3): 1, (2, 4): 2},
        frozenset(((3, 0), (3, 1), (3, 2), (3, 4), (3, 5),)),
        (4, 5), #destination              
        ),    


)