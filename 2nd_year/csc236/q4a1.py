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
##________________________________________________________________________________________________________________________
def rec(a):
	if a==0:
		return 1
	elif a==4:
		return 1
	elif a==6:
		return 1
	elif a==10:
		return 2
	elif a<4:
		return 0
	return rec(a-4)+rec(a-6)+rec(a-20)-rec(a-16)-rec(a-14)

for i in range(2,51,+2):
	print("T2() relationship: ",T2(i),"rec() relationship: ",rec(i))