from __future__ import print_function
import random
from math import inf

if hasattr(__builtins__, 'raw_input'):
    input = raw_input

def read_ints():
  return [int(x) for x in input().split()]

def read_int():
  return int(input())

def choices(seq, k=1):
  return [random.choice(seq) for _ in range(k)]


def distance(x,y,u,v):
  return abs(x-u) + abs(y-v)

def parcels(grid):
  offices = set()
  blanks = set()
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c]:
        offices.add((r,c))
      else:
        blanks.add((r,c))
  if len(blanks) <= 1:
    return 0
  
  blanks_list = list(blanks)
  best_dist = None
  for r,c in blanks_list:
    blanks.remove((r,c))
    offices.add((r,c))
    bottleneck = None
    for br,bc in blanks:
      local_min = min(distance(br,bc,pr,pc) for pr,pc in offices)
      if bottleneck is None or local_min > bottleneck:
        bottleneck = local_min
    offices.remove((r,c))
    blanks.add((r,c))
    if best_dist is None or bottleneck < best_dist:
      best_dist = bottleneck
  return best_dist


def parse_grid(grid_str):
  grid = [[True if c == "1" else False for c in r_str] for r_str in grid_str]
  offices = set()
  blanks = set()
  for r in range(len(grid)):
    for c in range((len(grid[0]))):
      if grid[r][c]:
        offices.add((r,c))
      else:
        blanks.add((r,c))
  return offices, blanks

def bfs(offices, R, C):
  from itertools import product
  distances = [[None for c in range(C)] for r in range(R)]
  max_dist = 0
  l1, l2 = offices, []
  dist = 0
  while True:
    for r, c in l1:
      if distances[r][c] is not None:
        continue
      distances[r][c] = dist
      max_dist = max(max_dist, dist)
      for dr, dc in [[0,1],[0,-1],[1,0],[-1,0]]:
        r1, c1 = r+dr, c+dc
        if r1 >= 0 and r1 < R and c1 >= 0 and c1 < C:
          l2.append((r1,c1))
    if l2 != []:
      l1, l2 = l2, []
      dist += 1
    else:
      break
  return distances, max_dist

def leq(blanks, distances, k):
  def change_coord(x,y):
    return -x+y, -x-y
  x_lb, x_ub = -inf, inf
  y_lb, y_ub = -inf, inf
  geq_k = [(r,c) for r,c in blanks if distances[r][c] >= k]
  for r,c in geq_k:
    x, y = change_coord(r,c)
    x_lb, x_ub = max(x, x_lb), min(x, x_ub)
    y_lb, y_ub = max(y, y_lb), min(y, y_ub)
  
  x_lb -= k
  x_ub += k
  y_lb -= k
  y_ub += k
  for r,c in blanks:
    x,y = change_coord(r,c)
    if x >= x_lb and x <= x_ub and y >= y_lb and y <= y_ub:
      return True
  return False

offices, blanks = parse_grid(["10000", "00000", "00000", "00110", "10000"])
distances, _ = bfs(offices,5,5)
leq(blanks, distances, 3)



def parcels_inspired(grid, R, C):
  offices, blanks = parse_grid(grid)
  if len(blanks) <= 1:
      return 0
  distances, k_ub = bfs(offices, R, C)
  k_lb = 0
  while k_lb != k_ub:
    k = (k_lb + k_ub) // 2
    if leq(blanks, distances, k):
      k_ub = k
    else:
      k_lb = k+1
  return k_lb

def parcels_main():
  T = read_int()
  for t in range(1,T+1):
    R,C = read_ints()
    grid = []
    for _ in range(R):
      row = input()
      grid.append(row)
    res = parcels(grid)
    print("Case #{}: {}".format(t, res))

# if __name__ == "__main__":
    # parcels_main()
    # print(parcels([[True, False], [False, True]]))
    # parcels([[True, False, True], [False, False, False], [True, False, True]])