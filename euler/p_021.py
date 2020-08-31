import math
def solve(l):
    def divisors(n):
        return [i for i in range(1, n) if n % i == 0]
    
    def amicable(n):
        d = sum(divisors(n))
        if n == sum(divisors(d)) and d >= n:
            return d
        else:
            return None
    
    s = 0
    for i in range(1, l+1):
        a = amicable(i)
        if a and a != i:
            print(i, a)
            s += (a+i)
    return s

    
            