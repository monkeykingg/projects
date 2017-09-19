from csp import *
from propagators import *
from course import *
from orderings import *

test_ord = False;
test_props = True;
test_mrv = True;
test_random = False;
test_dh = False;

c1 = Course('CSC108H1F20179')
c2 = Course('CSC148H1S20181')
c3 = Course('CSC165H1F20179')

c4 = Course('MAT137Y1Y20179')
c5 = Course('MAT223H1F20179')
c6 = Course('ECO101H1F20179')
c7 = Course('PSY100H1S20181')

c8 = Course('ECO102H1S20181')
c9 = Course('MAT224H1S20181')
c10 = Course('CSC236H1F20179')
c11 = Course('CSC263H1S20181')
c12 = Course('CSC258H1S20181')

c13 = Course('MAT235Y1Y20179')
c14 = Course('MAT237Y1Y20179')
c15 = Course('HPS100H1F20179')
c16 = Course('EAS256H1F20179')
c17 = Course('PHL245H1F20179')

c18 = Course('CSC343H1S20181')
c19 = Course('CSC369H1S20181')
c20 = Course('CSC373H1S20181')
c21 = Course('EAS257H1S20181')

course_list_1 = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c16,c21]
course_list_2 = [c8,c9,c10,c11,c13,c15,c17,c1,c2,c3]
course_list_3 = [c18,c19,c14,c15,c16,c17,c11,c13,c20]

# test cases
board = [course_list_1]

def print_soln(var_array, time_table_f, time_table_s):

    the_len = 0

    for row in var_array:
        assigned_val = row.get_assigned_value()
        if not assigned_val:
            print("======================================")
            print("No possible timetable can be generated")
            print("Please modify the input")
            print("======================================")
            return 0
        the_len = len(assigned_val.course_code[0:6] + assigned_val.section_code)

        for time in assigned_val.section_time:

            # check course type: year(Y) or fall(F) or winter(S)
            if assigned_val.course_code[8] == "Y":
                for i in range(time[1], time[2]):
                    time_table_f[time[0]][i] = assigned_val.course_code[0:6] + assigned_val.section_code
                    time_table_s[time[0]][i] = assigned_val.course_code[0:6] + assigned_val.section_code
            elif assigned_val.course_code[8] == "F":
                for i in range(time[1], time[2]):
                    time_table_f[time[0]][i] = assigned_val.course_code[0:6] + assigned_val.section_code
            else:
                for i in range(time[1], time[2]):
                    time_table_s[time[0]][i] = assigned_val.course_code[0:6] + assigned_val.section_code

    table_list_f = [['Monday     ','Tuesday    ','Wednesday  ','Thursday   ','Friday     ']]
    table_list_s = [['Monday     ', 'Tuesday    ', 'Wednesday  ', 'Thursday   ', 'Friday     ']]
    time_list_f = ['  Fall', '   9AM', '  10AM', '  11AM', '  12PM', '   1PM', '   2PM', '   3PM', '   4PM', '   5PM', '   6PM', '   7PM',
                   '   8PM']
    time_list_s = ['Winter', '   9AM', '  10AM', '  11AM', '  12PM', '   1PM', '   2PM', '   3PM', '   4PM', '   5PM',
                   '   6PM', '   7PM', '   8PM']

    for i in range(len(time_table_f[0])):
        temp = []
        for j in range(len(time_table_f)):
            temp.append(time_table_f[j][i])
        table_list_f.append(temp)

    for i in range(len(table_list_f)):
        for j in range(len(table_list_f[0])):
            if not table_list_f[i][j]:
                table_list_f[i][j] = "-" * the_len

    for i in range(len(time_table_s[0])):
        temp = []
        for j in range(len(time_table_s)):
            temp.append(time_table_s[j][i])
        table_list_s.append(temp)

    for i in range(len(table_list_s)):
        for j in range(len(table_list_s[0])):
            if not table_list_s[i][j]:
                table_list_s[i][j] = "-" * the_len

    print("========================================================================")

    for i in range(len(table_list_f)):
        temp = time_list_f[i] + '  '
        for j in range(len(table_list_f[0])):
            temp += table_list_f[i][j] + '  '
        print(temp)

    print("========================================================================")

    for i in range(len(table_list_s)):
        temp = time_list_s[i] + '  '
        for j in range(len(table_list_s[0])):
            temp += table_list_s[i][j] + '  '
        print(temp)


if __name__ == "__main__":

    time_table_f1 = [[None, None, None, None, None, None, None, None, None, None, None, None],  # Mon
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Tue
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Wed
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Thu
                    [None, None, None, None, None, None, None, None, None, None, None, None]]  # Fir

    time_table_s1 = [[None, None, None, None, None, None, None, None, None, None, None, None],  # Mon
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Tue
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Wed
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Thu
                    [None, None, None, None, None, None, None, None, None, None, None, None]]  # Fir

    time_table_f2 = [[None, None, None, None, None, None, None, None, None, None, None, None],  # Mon
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Tue
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Wed
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Thu
                    [None, None, None, None, None, None, None, None, None, None, None, None]]  # Fir

    time_table_s2 = [[None, None, None, None, None, None, None, None, None, None, None, None],  # Mon
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Tue
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Wed
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Thu
                    [None, None, None, None, None, None, None, None, None, None, None, None]]  # Fir

    time_table_f3 = [[None, None, None, None, None, None, None, None, None, None, None, None],  # Mon
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Tue
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Wed
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Thu
                    [None, None, None, None, None, None, None, None, None, None, None, None]]  # Fir

    time_table_s3 = [[None, None, None, None, None, None, None, None, None, None, None, None],  # Mon
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Tue
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Wed
                    [None, None, None, None, None, None, None, None, None, None, None, None],  # Thu
                    [None, None, None, None, None, None, None, None, None, None, None, None]]  # Fir

    if test_props:

        if test_mrv:
            for b in board:
                print("===========================================================")
                print("Solving board (MRV)")
                csp1, var_array1 = csp_model(b, 9, 11)
                print(var_array1)
                solver1 = BT(csp1)
                print("===========================================================")
                print("FC with MRV")
                solver1.bt_search(prop_FC, ord_mrv, val_arbitrary)
                print("GAC with MRV")
                solver1.bt_search(prop_GAC, ord_mrv, val_arbitrary)
                print("Solution")
                print_soln(var_array1, time_table_f1, time_table_s1)
                print("\n")

        if test_random:
            for b in board:
                print("===========================================================")
                print("Solving board (Random)")
                csp2, var_array2 = csp_model(b, 9, 11)
                solver2 = BT(csp2)
                print("===========================================================")
                print("FC with Random")
                solver2.bt_search(prop_FC, ord_random, val_arbitrary)
                print("GAC with Random")
                solver2.bt_search(prop_GAC, ord_random, val_arbitrary)
                print("Solution")
                print_soln(var_array2, time_table_f2, time_table_s2)
                print("\n")

        if test_dh:
            for b in board:
                print("===========================================================")
                print("Solving board (DH)")
                csp3, var_array3 = csp_model(b, 9, 11)
                solver3 = BT(csp3)
                print("===========================================================")
                print("FC with DH")
                solver3.bt_search(prop_FC, ord_dh, val_arbitrary)
                print("GAC with DH")
                solver3.bt_search(prop_GAC, ord_dh, val_arbitrary)
                print("Solution")
                print_soln(var_array3, time_table_f3, time_table_s3)
                print("===========================================================")

    if test_ord:

        a = Variable('A', [1])
        b = Variable('B', [1])
        c = Variable('C', [1])
        d = Variable('D', [1])
        e = Variable('E', [1])

        csp = CSP("Simple", [a, b, c, d, e])

        count = 0
        for i in range(0,len(csp.vars)):
            csp.vars[count].add_domain_values(range(0, count))
            count += 1

        var_1 = []
        var_2 = []
        var_3 = []

        var_1 = ord_mrv(csp)
        var_2 = ord_random(csp)
        var_3 = ord_dh(csp)

        if var_1:
            if((var_1.name) == csp.vars[0].name):
                print("Passed Ord MRV Test")
            else:
                print("Failed Ord MRV Test")
        else:
           print("No Variable Returned from Ord MRV")

        if var_2:
            if((var_2.name) == csp.vars[0].name):
                print("Passed Ord Random Test")
            else:
                print("Failed Ord Random Test")
        else:
           print("No Variable Returned from Ord Random")

        if var_3:
            if((var_3.name) == csp.vars[4].name):
                print("Passed Ord Degree Heuristic Test")
            else:
                print("Failed Ord Degree Heuristic Test")
        else:
           print("No Variable Returned from Ord Degree Heuristic")
