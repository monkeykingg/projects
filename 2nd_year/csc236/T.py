memo = {0:[""], 2:[], 4:["4"], 6:["6"], 10:["4+6", "10"]}

def T(n):
    if n in memo:
        return memo[n]
    else:
        partitions = []
        for i in range(4, n//2 + 1, 2):
            suffixes = T(n - i)
            for prefix in T(i):
                pre = [int(x) for x in prefix.split("+")]
                for suffix in suffixes:
                    suf = [int(x) for x in suffix.split("+")]
                    partitions.append("+".join([str(x) for x in sorted(pre + suf)]))
        memo[n] = sorted(set(partitions))
        return memo[n]

memo2 = dict()

def T2(n):
    if n not in memo2:
        if n < 24:
            memo2[n] = len(T(n))
        else:
            memo2[n] = T2(n-4) + T2(n-6) - T2(n-14) - T2(n-16) + T2(n-20)
    return memo2[n]