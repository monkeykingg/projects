""" Demonstrates how you can control a sorting function by giving it a function
to use when comparing two elements of the list.

Notice that we sort the list of strings by putting the ones that are
"smallest" in a sense at the front, but we later sort a list of dicts by
putting the ones that are "biggest" in a sense at the front. What determines
this orientation (ascending or descending order) is the return value from the
function we pass to sort. We simply need that function to return -1 if the
first argument should appear before the second argument in the final sorted
list, +1 if it should appear after, and 0 if their relative order doesn't
matter.

In this demo, and in the provided Twitter sorting function, we're using the
insertion sort algorithm. This could be replaced with any other sorting 
algorithm; we just chose one that you've already learned.
"""

def biggest_max(d1, d2):
    """ (dict of {object: int}, dict of {object: int}) -> int
    
    Return -1 if the maximum value in d1 is bigger than the maximum value in d2,
    1 if it is smaller, and 0 if they are equal.
    """
    
    d1_max = max(d1.values())
    d2_max = max(d2.values())
    if d1_max > d2_max:
        return -1
    elif d1_max < d2_max:
        return 1
    else:
        return 0
    
def shorter(s1, s2):
    """ (str, str) -> int
    
    Return -1 if string s1 is shorter than string s2, 1 if it is longer,
    and 0 if they have equal length.
    """
    
    if len(s1) < len(s2):
        return -1
    elif len(s1) > len(s2):
        return 1
    else:
        return 0
    
def my_sort(data, cmp):
    """ (list of objects, function) -> NoneType
    
    Sort the data list using the comparison function cmp.
    """
    
    # Insertion sort
    for i in range(1, len(data)):
        current = data[i]
        position = i
        while position > 0 and cmp(data[position - 1], current) > 0:
            data[position] = data[position - 1]
            position = position - 1 
        data[position] = current 
    
if __name__ == "__main__":
    
    L = ["Once", "upon", "a", "time", "there", "was", "a", "curious", "girl"]
    
    # Sort the list using Python's default behaviour. 
    # It will sort alphabetically, first uppercase, then lowercase letters.
    L.sort()
    print(L)
    
    # Now sort it so that we control how pairs of list items are compared.
    # Tell sort to compare using function shorter.  The shorter strings
    # will be at the front of the updated list.
    my_sort(L, shorter)
    print(L)
    
    # Now try sorting a list of dictionaries.
    L2 = [{"Jo": 2, "Nate": 99, "Mari": 45}, {"Zara": 2}, 
          {"Reuben": 54,"Zoya": 11, "Jiaqi": 9}, {"Myrka": 23, "Harbinder": 18}]
    
    # We actually can't sort a list of dictionaries using Python's default sort. 
    # How would it decide how to order the dictionaries?
    # Uncomment the line below to see the error.
    #L2.sort()
    print(L2)
    
    # Now tell Python to sort using the biggest_max function.  Dictionaries
    # whose maximum key is largest will be at the front of the updated list.
    my_sort(L2, biggest_max)
    print(L2)