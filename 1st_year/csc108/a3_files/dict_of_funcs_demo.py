""" Demonstrates how you can create a dictionary where the values are functions.

You may find this useful in writing cleaner code in your Assignment 3 solution.
This way of calling functions will eliminate the need for a number of 
if/elif/else statements, replacing them with much shorter code.
"""

def function_a(value):
    return value + 1

def function_b(value):
    return value + 2

def function_c(value):
    return value + 10

if __name__ == '__main__':
    letter_to_funcs = {'a': function_a, 'b': function_b, 'c': function_c}
    
    # No error checking - assumes only 'a', 'b', or 'c' will be input
    letter = input('Enter the letter a, b, or c: ')    
    
    # Call the function by looking up the one associated with the key in the dict
    result = letter_to_funcs[letter](5)
    
    print(result)