from math import ceil, floor, sqrt
import itertools
from collections import Counter

try:
    input = raw_input
except NameError:
    pass

def read_ints():
  return [int(i) for i in raw_input().split()]

def read_int_arr():
  return list(map(int, raw_input().split()))

def read_input():
  num_cases = int(input())
  for t in range(1, num_cases+1):
    length = input()
    xs = read_int_arr()
    res = solve(xs)
    print("Case #{}: {}".format(t, res))

def solve(xs):
  m = int(ceil(sqrt( max(xs) * len(xs) )))
  squares = [i*i for i in range(m+1)]
  ct = Counter() # map partial sum |-> count
  ct[0] = 1
  ps = 0 # current partial sum
  res = 0
  for i, x in enumerate(xs):
    ps += x
    for s in squares:
      desired = ps - s
      n_d = ct[desired]
      res += n_d
    ct[ps] += 1
  return res

if __name__ == "__main__":
  read_input()