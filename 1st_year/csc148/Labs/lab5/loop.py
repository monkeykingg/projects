def dot_prod(u, v):
    """
    Return the dot product of u and v

    @param list[float] u: vector of floats
    @param list[float] v: vector of floats
    @rtype: float

    >>> dot_prod([1.0, 2.0], [3.0, 4.0])
    11.0
    """
    result = []
    for i in range(len(u)):
        mul_num = u[i] * v[i]
        result.append(mul_num)
    return sum(result)

def matrix_vector_prod(m, u):
    """
    Return the matrix-vector product of m x u

    @param list[list[float]] m: matrix
    @param list[float] u: vector
    @rtype: list[float]
    >>> matrix_vector_prod([[1.0, 2.0], [3.0, 4.0]], [5.0, 6.0])
    [17.0, 39.0]
    """
    result = []
    for item in m:
        temp = dot_prod(item, u)
        result.append(temp)
    return result

def pythagorean_triples(n):
    """
    Return list of pythagorean triples as non-descending tuples
    of ints from 1 to n.

    Assume n is positive.

    @param int n: upper bound of pythagorean triples

    >>> pythagorean_triples(5)
    [(3, 4, 5)]
    """
    for i in range(1, n+1):
        for j in range(1, n+1):
            for k in range(1, n+1):
                if i*i + j*j == k*k and i <= j <= k:
                    result = (i, j, k)
                    return [result]
