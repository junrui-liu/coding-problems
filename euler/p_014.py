#!/usr/bin/env python3

"""
The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""

maximum = 1000000
seq = [(-1, -1, []) for i in range(maximum+1)]

seq[1] = (1, 0, [])

for i in range(2, maximum+1):
    print(i, end=' -> ')
    n = i
    prev, count, i_next = seq[i]
    if prev < 0:
        while True:
            n = n//2 if n%2 == 0 else 3*n+1
            count += 1
            if n <= maximum:
                _, _, n_next = seq[n]
                n_next.append(i)
                print(n, end='\n')
                seq[i] = (n, count, sorted(n_next))
                break

def collapse(i):
    i_prev, i_count, i_next = seq[i]
    for j in i_next:
        j_prev, j_count, j_next = seq[j]
        seq[j] = (j_prev, i_count+j_count, j_next)

for i in range(2, maximum+1):
    collapse(i)

most = -1
most_n = -1
for i in range(2, maximum+1):
    i_prev, i_count, i_next = seq[i]
    if i_count > most:
        most = i_count
        most_n = i


def naive():
    for i in range(1, maximum+1):
        n = i
        count = 0
        while n != 1:
            n = n//2 if n%2 == 0 else 3*n+1
            count += 1
        if count > most:
            print(i, count)
            most = count
            most_n = i
