#Look for #IMPLEMENT tags in this file.

'''
Construct and return Kenken CSP model.
'''

from cspbase import *
import itertools

# get permutation list
def perm(domain, length):
    result = []
    for item in itertools.permutations(domain, length):
        result.append(item)
    return result

# get repetition permutation list
def perm_rep(dom, length):
    result = []
    for t in itertools.product(dom, repeat=length):
        result.append(t)
    return result

# check and return those girds satisfy operation and goal
def cageCheck(dom, num_of_grid, op, goal):

    result = set()
    tuples = perm_rep(dom, num_of_grid)

    for t in tuples:
        if len(t) > 0:
            temp = t[0]

            for i in range (1, len(t)):
                # add
                if op == 0:
                    temp += t[i]
                # subtract
                elif op == 1:
                    temp -= t[i]
                # divide
                elif op == 2:
                    temp /= t[i]
                # multiply
                elif op == 3:
                    temp *= t[i]

            if temp == goal:
                t_set = set(perm(t, len(t)))
                result = result.union(t_set)

    return tuple(result)

def kenken_csp_model(kenken_grid):
    '''Returns a CSP object representing a Kenken CSP problem along
       with an array of variables for the problem. That is return

       kenken_csp, variable_array

       where kenken_csp is a csp representing the kenken model
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the board (indexed from (0,0) to (N-1,N-1))


       The input grid is specified as a list of lists. The first list
	   has a single element which is the size N; it represents the
	   dimension of the square board.

	   Every other list represents a constraint a cage imposes by
	   having the indexes of the cells in the cage (each cell being an
	   integer out of 11,...,NN), followed by the target number and the
	   operator (the operator is also encoded as an integer with 0 being
	   '+', 1 being '-', 2 being '/' and 3 being '*'). If a list has two
	   elements, the first element represents a cell, and the second
	   element is the value imposed to that cell. With this representation,
	   the input will look something like this:

	   [[N],[cell_ij,...,cell_i'j',target_num,operator],...]

       This routine returns a model which consists of a variable for
       each cell of the board, with domain equal to {1-N}.

       This model will also contain BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.) and an n-ary constraint for each cage in the grid.
    '''

    ##IMPLEMENT

    # n x n size of kenken game board
    n = kenken_grid[0][0]

    # domain
    dom = []
    for i in range(n):
        dom.append(i+1)

    variable_array = []

    # list of all variables
    vars = []

    # build variable_array and vars
    for i in dom:
        row = []
        for j in dom:
            v = Variable('V{}{}'.format(i, j), dom)
            vars.append(v)
            row.append(v)
        variable_array.append(row)

    cons = []

    # rows and columns should satisfy sudoku rules
    for i in range(n):

        # find all variables in one row/column/cage
        row_vars = vars[(i * n): ((i + 1) * n)]
        col_vars = []
        for j in range(n):
            col_vars.append(vars[i + (j * n)])

        # build constraint by 2 variables in one row
        for var_pair in itertools.combinations(row_vars, 2):
            con = Constraint("C-{},{})".format(var_pair[0].name,
                                               var_pair[1].name),
                                               [var_pair[0], var_pair[1]])
            sat_tuples = []
            for t in itertools.product(var_pair[0].cur_domain(),
                                       var_pair[1].cur_domain()):
                # sudoku check
                if t[0] != t[1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        # build constraint by 2 variables in one column
        for var_pair in itertools.combinations(col_vars, 2):
            con = Constraint("C-{},{})".format(var_pair[0].name,
                                               var_pair[1].name),
                                               [var_pair[0], var_pair[1]])
            sat_tuples = []
            for t in itertools.product(var_pair[0].cur_domain(),
                                       var_pair[1].cur_domain()):
                # sudoku check
                if t[0] != t[1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    # cage
    for cage in kenken_grid[1:]:

        # when there are 2 elements, then first element corresponds to a cell
        # the second element is the value enforced on the cell
        if len(cage) == 2:
            i = int(str(cage[0])[0])
            j = int(str(cage[0])[1])
            var = variable_array[i-1][j-1]
            name = "V{}{}".format(i, j)
            con = Constraint("C-{}".format(name), [var])
            sat_tuples = []
            for item in dom:
                if item == cage[-1]:
                    sat_tuples.append((item,))
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        # when there are more than 3 elements, the last element shows the type
        # of operations, the second last element is the goal value we need to
        # reach
        else:
            num_of_grid = len(cage) - 2
            op = cage[-1]
            goal = cage[-2]
            name = ""
            con_name = ""
            vs = []
            for item in cage[:-2]:
                i = int(str(item)[0])
                j = int(str(item)[1])
                var = variable_array[i-1][j-1]
                vs.append(var)
                name += "V{}{}".format(i, j)
                con_name += "C-{}".format(name)
            con = Constraint(con_name, vs)
            sat_tuples = cageCheck(dom, num_of_grid, op, goal)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)


    kenken_csp = CSP("kenken csp", vars)
    for c in cons:
        kenken_csp.add_constraint(c)

    return kenken_csp, variable_array
