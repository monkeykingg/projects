#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import propagators

'''
This file will contain the MRV variable ordering heuristic to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
'''


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.
    MRV returns the variable with the most constrained current domain
    (i.e., the variable with the fewest legal values).
    '''

    min_domain = -1
    min_variable = None

    for item in csp.get_all_unasgn_vars():
        if min_domain < 0:
            min_domain = item.cur_domain_size()
            min_variable = item
        elif item.cur_domain_size() < min_domain:
            min_domain = item.cur_domain_size()
            min_variable = item

    return min_variable

def ord_random(csp):
    '''
    ord_random(csp):
    Returns a Variable object var at random.
    Returned var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var

def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    Returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_dh(csp):
    '''
    ord_dh(csp):
    Select variable that is involved in largest number of constraints on other unassigned variables (lecture).
    Returns the variable whose node has highest degree (definition).
    '''

    result = []
    for var in csp.get_all_unasgn_vars():
        record = []
        for cons in csp.get_cons_with_var(var):
            for cons_var in cons.get_scope():
                if cons_var != var:
                    if cons_var not in record:
                        if not cons_var.is_assigned():
                            record.append(cons_var)
        total = len(record)
        result_tuple = (var, total)
        result.append(result_tuple)
    final_result = sorted(result, key=lambda x: x[1])
    var = final_result[-1][0]
    return var
