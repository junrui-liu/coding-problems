import itertools
import math

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

