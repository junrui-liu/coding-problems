#!/usr/bin/env python3
from collections import defaultdict

def read_ints():
  return [int(i) for i in input().split()]

def print_wall(wall):
  print('\n'.join((''.join(map(str,r)) for r in wall[::-1])))

def topo_sort(graph):
  time = 0
  visited = {key: False for key in graph}
  on_path = {key: False for key in graph}
  finishing_time = {key: None for key in graph}

  def dfs(v):
    # print(v)
    assert(not on_path[v])
    if visited[v]:
      return
    on_path[v] = True
    visited[v] = True
    for w in graph[v]:
      dfs(w)
    nonlocal time
    finishing_time[v] = time
    # print(v, "finishes at time ", time)
    on_path[v] = False
    time += 1

  for key in graph:
    if not visited[key]:
      dfs(key)
  
  fst, snd = lambda p: p[0], lambda p: p[1]
  finishing_time_sorted = sorted([(key,ft) for (key, ft) in finishing_time.items()], key=snd)
  schedule = list(map(fst, finishing_time_sorted))
  return schedule

def read_input():
  BOT = '_' # chr(ord('A')-1)
  num_cases = int(input())
  for t in range(num_cases):
    r, c = read_ints()
    bottom = BOT * c
    positions = defaultdict(set)
    wall = [[None for _c in range(c)] for _r in range(r+1)]
    for i in range(r,-1,-1):
      row = bottom if i == 0 else input()
      for j, key in enumerate(row):
        wall[i][j] = key
        positions[key].add((i,j))
  
    def solve(positions, wall):
      depend = {key: set() for key in positions}
      for key in positions:
        for i,j in positions[key]:
          if i > 0:
            key_below = wall[i-1][j]
            if key_below != key:
              depend[key].add(key_below)
      try:
        schedule = topo_sort(depend)
        schedule = [k for k in schedule if k != BOT]
        return ''.join(map(str, schedule))
      except AssertionError:
        return -1

    print("Case #{}: {}".format(t, solve(positions, wall)))

if __name__ == "__main__":
  read_input()