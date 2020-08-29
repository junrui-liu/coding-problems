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
    N, Q = read_ints()
    xs = read_int_arr()
    res = []
    for q in range(Q):
      S, K = read_ints()
      res.append(solve(xs, S, K))
    print("Case #{}: {}".format(t, ' '.join(map(str, res))))

DIR_L = 0
DIR_R = 1
FST = 1
SND = 2


def sss(d, N):
  """Return three functions: ok, stepn, and step"""
  if d == DIR_L:
    return lambda i: i >= 0, lambda i,n: i-n, lambda i: i-1
  else:
    return lambda i: i < N, lambda i,n: i+n, lambda i: i+1

def survey(xs, d):
  N = len(xs)
  ok, stepn, step = sss(d, N)
  cnt = [1 for _ in range(N)]
  start = N-1 if d == DIR_L else 0
  stk = [(start, FST)]
  while len(stk) > 0:
    i, e = stk.pop()
    hi = xs[i]
    j = step(i)
    if e == FST and ok(j):
      hj = xs[j]
      if xs[i] > xs[j]: # does not hit a wall
        stk.append((i, SND))
      stk.append((j, FST))
    elif e == SND:
      j = step(i)
      hj = xs[j]
      cj = cnt[j]
      cnt[i] += cj
      j = stepn(j,cj)
      while ok(j):
        hj = xs[j]
        cj = cnt[j]
        if xs[i] > xs[j]:
          cnt[i] += cj
        j = stepn(j,cj)
  return cnt

def solve(xs, room, kth_room):
  room -= 1 # convert to 0-index
  k = kth_room-1 # k doors left
  if k == 0: return room+1
  doors = []
  cl, cr = survey(xs, DIR_L), survey(xs, DIR_R)
  N = len(xs)
  ok_l, stepn_l, _ = sss(DIR_L, N)
  ok_r, stepn_r, _ = sss(DIR_R, N)
  i, j = room-1, room # choose btw left door i or right door j
  # Batch-open doors, if any, until k reaches 0
  while ( ok_l(i) or ok_r(j) ) and k > 0:
    k0 = k # remember the last d
    # Open the left door if reached right end, or if left door is easier
    if not ok_r(j) or ( ok_l(i) and xs[i] < xs[j] ):
      doors.append((i, DIR_L))
      l, r = cl[i], 0
    else: # open the right door otherwise
      doors.append((j, DIR_R))
      l, r = 0, cl[j]
    k -= l + r
    i, j = stepn_l(i,l), stepn_r(j,r)
  last_door, d = doors[-1]
  if d == DIR_L:
    room = last_door + 1
    room = stepn_l(room, k0)
  else:
    room = last_door
    room = stepn_r(room, k0)
  return room+1

def large_test():
  import random
  L = 200000
  l = list(range(L))
  random.shuffle(l)
  print()
  print(solve(l, random.randint(0,L), L))

print(solve([9, 3, 4, 6], 3, 1))

if __name__ == "__main__":
  read_input()