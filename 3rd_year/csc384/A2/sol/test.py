
import itertools

def test(kenken_grid):
    n = kenken_grid[0][0]

    dom = []
    for i in range(n):
        dom.append(i + 1)

    vars = []
    for i in dom:
        for j in dom:
            vars.append('V{}{}'.format(i, j))

    cons = []

    for i in range(n):
        vars_row = vars[(i * n): ((i + 1) * n)]
        vars_col = []
        for j in range(n):
            vars_col.append(vars[i + (j * n)])

        for var_pair in itertools.combinations(vars_row, 2):
            cons.append("C-{},{})".format(var_pair[0],var_pair[1]))

        for var_pair in itertools.combinations(vars_col, 2):
            cons.append("C-{},{})".format(var_pair[0],var_pair[1]))
    return cons
