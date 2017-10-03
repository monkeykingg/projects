def brute(Array):
    L = []
    for i in range(len(Array)):
        for j in range(len(Array)):
            L.append(sum(Array[i:j+1]))
    return max(L)

def divide(Array, begin, end):
    if begin > end:
        return -2**31
    mid = (begin + end) // 2  
    Leftmax = divide(Array, begin, mid-1)
    Rightmax = divide(Array, mid+1, end)       
    result = max(Leftmax,Rightmax)
    summation = 0
    midleftmax = 0
    for i in range(begin, mid)[::-1]:
        summation += Array[i]
        if(summation > midleftmax):
            midleftmax = summation
    summation = 0
    midrightmax = 0
    for i in range(mid+1, end+1):
        summation += Array[i]
        if(summation > midrightmax):
            midrightmax = summation
    result = max(result, midleftmax + midrightmax + Array[mid])
    return result