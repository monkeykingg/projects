#Look for #IMPLEMENT tags in this file.

'''
Construct and return Kenken CSP model.
'''

from cspbase import *
import itertools
record = []

def _get_sat_tuples(variable1, variable2):
    #print('-------- {} | {} --------'.format(variable1, variable2))
    lst = []
    for section1 in variable1.domain():
        for section2 in variable2.domain():
            if not section1.is_overlap(section2):
                lst.append((section1, section2))
                #print(' ' * 5, section1, section2)
    return lst


def csp_model(course_list, start, end):
    """

    :param course_list:
    :param work_load: the max hours you can study in a day
    :param prefer_time: "daytime" or "night"
    :return:

    format of output/input course_grid_list: [[course_code,(x, x, x),(x, x, x)],[course_code,(x, x, x)]]
    format of output/input course_list: [course_code, course_code, course_code]]
    """

    # Create variables, each variable is a type of event for one course.
    vars = []
    for c in course_list:
        if c not in record:
            for section_type, sections in c.sections.items():
                vars.append(Variable('{}'.format(c.course_code + '-' + section_type), sections[:]))
            record.append(c)

    cons = []
    for i in range(len(vars)):
        for j in range(i + 1, len(vars)):
            var1, var2 = vars[i], vars[j]
            if (var1.name[8] == var2.name[8]) or var1.name[8] == 'Y' or var2.name[8] == 'Y':
                con = Constraint("C({} {})".format(var1, var2), [var1, var2])
                con.add_satisfying_tuples(_get_sat_tuples(var1, var2))
                cons.append(con)

    if start and end:
        for i in range(len(vars)):
            con = Constraint("C({} TIME)".format(vars[i]), [vars[i]])
            sat_tup = []
            for sec in vars[i].domain():
                count = 0
                for sec_time in sec.section_time:
                    if sec_time[1] > end or sec_time[2] <= start:
                        count += 1

                if count == len(sec.section_time):
                    sat_tup.append((sec,))

            con.add_satisfying_tuples(sat_tup)
            cons.append(con)

    csp = CSP("TimeTable", vars)
    for c in cons:
        csp.add_constraint(c)

    return csp, vars
