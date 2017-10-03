
def closestPair(points):
    n = len(points)
    distance = pow(points[0][0] - points[1][0], 2) + pow(points[0][1] - points[1][1], 2)
    closest_pair = (points[0], points[1])
    i = 0
    while i < n:
        closest_pair = helper(points, i, distance, closest_pair)
        i += 1
    return closest_pair


def helper(points, i, distance, closest_pair):
    j = i + 1
    n = len(points)
    while i < j < n:
        temp = pow(points[i][0] - points[j][0], 2) + pow(points[i][1] - points[j][1], 2)
        if temp < distance and i != j:
            distance = temp
            closest_pair = (points[i], points[j])
        j += 1  
    return closest_pair