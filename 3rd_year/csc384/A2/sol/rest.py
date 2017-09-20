def cageCheck(val_com, op, goal):

    # add
    if op == 0:
        if goal == sum(val_com):
            return True

    # subtract
    if op == 1:
        for i in range(len(val_com)):
            sub = val_com[i]
            temp = list(val_com).copy()
            temp.pop(i)
            sub_total = 0
            for item in temp:
                sub_total += item
            if abs(sub - sub_total) == goal:
                return True

    # divide
    if op == 2:
        for i in range(len(val_com)):
            divisor_1 = val_com[i]
            temp = list(val_com).copy()
            temp.pop(i)
            divisor_2 = 1
            for item in temp:
                divisor_2 = divisor_2 * item
            cond_1 = divisor_1 / divisor_2 == goal
            cond_2 = divisor_1 % divisor_2 == 0
            cond_3 = divisor_2 / divisor_1 == goal
            cond_4 = divisor_2 % divisor_1 == 0
            if (cond_1 and cond_2) or (cond_3 and cond_4):
               return True

    # multiply
    if op == 3:
        result = 1
        for item in val_com:
            result = result * item
        if result == goal:
            return True

    return False


'''    for i in range(len(cages)):
        if (len(cages[i]) == 2) or (len(cages[i]) == 3):
            v = Variable('V{}{}'.format((cage[0] / 10), (cage[0] % 10)), [cage[1]])
            con = Constraint("C-{}".format(v.name), [v])
            con.add_satisfying_tuples([()])
            cons.append(con)
        else:
            name = "C-"
            val = []
            for v in cage_vars[i]:
                name = name + v.name + ','
                val.append(v.cur_domain())
            con = Constraint(name, [cage_vars[i][0], cage_vars[i][len(cage_vars[i])-2]])
            sat_tuples = []
            for val_com in itertools.permutations(val, len(cage) - 2):
                if cageCheck(val_com, cage_vars[i][-1], cage_vars[i][-2]):
                    sat_tuples.append(val_com)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)
'''


def FCCheck(c, x, prunedVar):
    for item in x.cur_domain():
        if c.has_support(x, item) == False:
            x.prune_value(item)
            prunedVar.append((x, item))
        if x.domain_size() == 0:
            return True
    return False



cons = []

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

row = 1
    row_times = 0
    row_starter = 1
    while row_times != n:
        if row_starter == 1:
            i = 1
        else:
            i = row_starter
        start = row_starter
        for i in range(i, n):
            for j in range(start, n):
                row_con = Constraint("C-V{}{}V{}{}".format(row, i, row, j + 1),[variable_array[row - 1][i - 1], variable_array[row - 1][j]])
                column_con = Constraint("C-V{}{}V{}{}".format(i, row, j + 1, row),[variable_array[i - 1][row - 1], variable_array[j][row - 1]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] != t[1]:
                        sat_tuples.append(t)

                row_con.add_satisfying_tuples(sat_tuples)

                column_con.add_satisfying_tuples(sat_tuples)

                cons.append(row_con)
                cons.append(column_con)
            start += 1
        row_times += 1
        row += 1
