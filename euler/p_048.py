modulo = 10000000000
s = 0
for i in range(1, 1000+1):
    p = 1
    for j in range(1, i+1):
        p *= i
        p %= modulo
    s += p
    s %= modulo


