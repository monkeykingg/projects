# recursion exercises with nested lists


def gather_lists(list_):
    """
    Return the concatenation of the sublists of list_.

    @param list[list] list_: list of sublists
    @rtype: list

    >>> list_ = [[1, 2], [3, 4]]
    >>> gather_lists(list_)
    [1, 2, 3, 4]
    """
    # this is a case where list comprehension gets a bit unreadable
    new_list = []
    for sub in list_:
        for element in sub:
            new_list.append(element)
    return new_list


def list_all(obj):
    """
    Return a list of all non-list elements in obj or obj's sublists, if obj
    is a list.  Otherwise, return a list containing obj.

    @param list|object obj: object to list
    @rtype: list

    >>> obj = 17
    >>> list_all(obj)
    [17]
    >>> obj = [1, 2, 3, 4]
    >>> list_all(obj)
    [1, 2, 3, 4]
    >>> obj = [[1, 2, [3, 4], 5], 6]
    >>> all([x in list_all(obj) for x in [1, 2, 3, 4, 5, 6]])
    True
    >>> all ([x in [1, 2, 3, 4, 5, 6] for x in list_all(obj)])
    True
    """
    if not isinstance(obj, list):
        return [obj]
    result = []
    for item in obj:
        result += list_all(item)
    return result


def max_length(obj):
    """
    Return the maximum length of obj or any of its sublists, if obj is a list.
    otherwise return 0.

    @param object|list obj: object to return length of
    @rtype: int

    >>> max_length(17)
    0
    >>> max_length([1, 2, 3, 17])
    4
    >>> max_length([[1, 2, 3, 3], 4, [4, 5]])
    4
    """
    if not isinstance(obj, list):
        return 0
    result = [len(obj)]
    for item in obj:
        result.append(max_length(item))
    return max(result)


def list_over(obj, n):
    """
    Return a list of strings of length greater than n in obj, or sublists of obj, if obj
    is a list.  Otherwise, if obj is a string return a list containing obj if obj has
    length greater than n, otherwise an empty list.

    @param str|list obj: possibly nested list of strings, or string
    @param int n: non-negative integer
    @rtype: list[str]

    >>> list_over("five", 3)
    ['five']
    >>> list_over("five", 4)
    []
    >>> L = list_over(["one", "two", "three", "four"], 3)
    >>> all([x in L for x in ["three", "four"]])
    True
    >>> all([x in ["three", "four"] for x in L])
    True
    """
    if not isinstance(obj, list):
        if len(obj) > n:
            return [obj]
        else:
            return []
    result = []
    for item in obj:
        result += list_over(item, n)
    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
