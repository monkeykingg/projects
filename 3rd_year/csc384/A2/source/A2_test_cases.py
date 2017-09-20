from kenken_csp import *
from propagators import *
from orderings import *

test_ord_mrv = True;
test_props = False;

boards = [ [[3],[11,21,3,0],[12,22,2,1],[13,23,33,6,3],[31,32,5,0]],
[[4],[11,21,6,3],[12,13,3,0],[14,24,3,1],[22,23,7,0],[31,32,2,2],[33,43,3,1],[34,44,6,3],[41,42,7,0]],
[[5],[11,21,4,1],[12,13,2,2],[14,24,1,1],[15,25,1,1],[22,23,9,0],[31,32,3,1],[33,34,44,6,3],[35,45,9,0],[41,51,7,0],[42,43,3,1],[52,53,6,3],[54,55,4,1]],
[[6],[11,21,11,0],[12,13,2,2],[14,24,20,3],[15,16,26,36,6,3],[22,23,3,1],[25,35,3,2],[31,32,41,42,240,3],[33,34,6,3],[43,53,6,3],[44,54,55,7,0],[45,46,30,3],[51,52,6,3],[56,66,9,0],[61,62,63,8,0],[64,65,2,2]] ]

def print_kenken_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":
    
    if test_props:        
        for b in boards:
            print("Solving board")
            csp, var_array = kenken_csp_model(b)
            solver = BT(csp)
            print("=======================================================")
            print("FC")
            solver.bt_search(prop_FC)
            #print("GAC")
            #solver.bt_search(prop_GAC)
            print("Solution")
            print_kenken_soln(var_array)

    if test_ord_mrv:

        a = Variable('A', [1])
        b = Variable('B', [1])
        c = Variable('C', [1])
        d = Variable('D', [1])
        e = Variable('E', [1])

        simpleCSP = CSP("Simple", [a,b,c,d,e])

        count = 0
        for i in range(0,len(simpleCSP.vars)):
            simpleCSP.vars[count].add_domain_values(range(0, count))
            count += 1

        var = []
        var = ord_mrv(simpleCSP)

        if var:
            if((var.name) == simpleCSP.vars[0].name):
                print("Passed First Ord MRV Test")
            else:
                print("Failed First Ord MRV Test") 
        else:
           print("No Variable Returned from Ord MRV") 

        a = Variable('A', [1,2,3,4,5])
        b = Variable('B', [1,2,3,4])
        c = Variable('C', [1,2])
        d = Variable('D', [1,2,3])
        e = Variable('E', [1])

        simpleCSP = CSP("Simple", [a,b,c,d,e])

        var = []
        var = ord_mrv(simpleCSP)

        if var:
            if((var.name) == simpleCSP.vars[len(simpleCSP.vars)-1].name):
                print("Passed Second Ord MRV Test")
            else:
                print("Failed Second Ord MRV Test") 
        else:
           print("No Variable Returned from Ord MRV") 
