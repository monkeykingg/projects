#Look for #IMPLEMENT tags in this file.

'''
Construct and return Kenken CSP model.
'''

from cspbase import *
import itertools

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
    
    
