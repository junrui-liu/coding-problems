total = 0
for i in range(2, 9**5*8):
    j = i
    s = 0
    while i != 0:
        s += (i%10)**5
        i = i // 10
    if s == j:
        print(s)
        total += s
print(total)