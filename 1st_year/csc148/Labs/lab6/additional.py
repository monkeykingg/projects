def list_even(obj):
    """
    Return a list of all event integers in obj or sublists of obj, if obj is a list.
    Otherwise, if obj is an even integer return a list containing obj, and if obj
    is an odd integer, return an empty list.

    @param int|list obj: possibly nested list of ints, or int
    @rtype: list[int]

    >>> list_even(3)
    []
    >>> list_even(16)
    [16]
    >>> L = list_even([1, 2, 3, 4, 5])
    >>> all([x in L for x in [2, 4]])
    True
    >>> all([x in [2, 4] for x in L])
    True
    >>> L = list_even([1, 2, [3, 4], 5])
    >>> all([x in L for x in [2, 4]])
    True
    >>> all([x in [2, 4] for x in L])
    True
    >>> L = list_even([1, [2, [3, 4]], 5])
    >>> all([x in L for x in [2, 4]])
    True
    >>> all([x in [2, 4] for x in L])
    True
    """
    if not isinstance(obj, list):
        if obj % 2 != 0:
            return []
        else:
            return [obj]
    result = []
    for item in obj:
        result += list_even(item)
    return result


def count_even(obj):
    """
    Return the number of even numbers in obj or sublists of obj
    if obj is a list.  Otherwise, if obj is a number, return 1
    if it is an even number and 0 if it is an odd number.

    @param int|list obj: object to count even numbers from
    @rtype: int

    >>> count_even(3)
    0
    >>> count_even(16)
    1
    >>> count_even([1, 2, [3, 4], 5])
    2
    """
    if not isinstance(obj, list):
        if obj % 2 != 0:
            return 0
        else:
            return 1
    result = 0
    for item in obj:
        result += count_even(item)
    return result


def count_all(obj):
    """
    Return the number of elements in obj or sublists of obj if obj is a list.
    Otherwise, if obj is a non-list return 1.

    @param object|list obj: object to count
    @rtype: int

    >>> count_all(17)
    1
    >>> count_all([17, 17, 5])
    3
    >>> count_all([17, [17, 5], 3])
    4
    """
    if not isinstance(obj, list):
        return 1
    result = 0
    for item in obj:
        result += count_all(item)
    return result


def count_above(obj, n):
    """
    Return tally of numbers in obj, and sublists of obj, that are over n, if
    obj is a list.  Otherwise, if obj is a number over n, return 1.  Otherwise
    return 0.

    >>> count_above(17, 19)
    0
    >>> count_above(19, 17)
    1
    >>> count_above([17, 18, 19, 20], 18)
    2
    >>> count_above([17, 18, [19, 20]], 18)
    2
    """
    if not isinstance(obj, list):
        if obj > n:
            return 1
        else:
            return 0
    return sum([count_above(item, n) for item in obj])
