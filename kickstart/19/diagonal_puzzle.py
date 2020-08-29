# Input template

try:
    input = raw_input
except NameError:
    pass

def read_ints():
  return [int(i) for i in raw_input().split()]

def read_int_arr():
  return list(map(int, raw_input().split()))

def explode(s):
  return [ch for ch in s]

def read_input():
  num_cases = int(input())
  for t in range(1, num_cases+1):
    N = int(input())
    board = read_board(N)
    res = solve(board, N)
    print("Case #{}: {}".format(t, res))

# Problem-specific helpers
BLACK = "#"
WHITE = "."
def read_board(N):
  return [explode(input()) for _ in range(N)]

def generate_board(n, black=BLACK, white=WHITE):
  import random
  randbool = lambda: random.random() < 0.5
  return [[black if randbool() else white for i in range(n)] for j in range(n)]

def board_to_str(board):
  return '\n'.join([''.join(line) for line in board])

# Solution begins here
from collections import defaultdict

def pts_on_forward_diag(d, N):
  if d < N:
    n = d+1 # number of pts on this diagonal
    i, j = 0, d
  else:
    n = 2*N - d - 1
    i, j = d-N+1, N-1
  for _ in range(n):
    yield (i,j)
    i, j = i+1, j-1

def pts_on_diag(d, N):
  num_diag = 2*N-1
  if d < num_diag: # forward diagonal
    for i,j in pts_on_forward_diag(d, N):
      yield i,j
    # return pts_on_forward_diag(d, N)
  else: # backward diagonal: simply reflect in the horizontal midline
    for i,j in pts_on_forward_diag(d - num_diag, N):
      yield i, N-j-1

def which_diag(i, j, dir, N):
  if dir == 1:
    return i + j
  else:
    return which_diag(i, N-j-1, 1, N) + 2*N - 1

def bipartite(g, m):
  visited = defaultdict(lambda: False)
  def dfs(v, c, colors, ct):
    visited[v] = True
    colors[v] = c
    if v < m: color_count[c] += 1 # do not count dummy nodes
    if v in g:
      for w in g[v]:
        if visited[w]:
          assert(colors[w] == 1-c)
        else:
          dfs(w, 1-c, colors, color_count)
  total = 0
  for v in range(m):
    if not visited[v]:
      colors = dict()
      color_count = [0,0]
      dfs(v, 0, colors, color_count)
      total += min(color_count)
  return total

def solve(board, N):
  # print(board, N)
  num_diag = (2*N - 1) * 2
  forward = 1
  backward = -1

  # 2-coloring the xor graph of diagonals
  g = defaultdict(set)
  def xor(v, w):
    g[v].add(w)
    g[w].add(v)
  # counter to generate fresh dummy diagonal names
  ct = num_diag
  # loop through forward diagonals
  for d in range(num_diag//2):
    for (i,j) in pts_on_diag(d,N):
      d2 = which_diag(i, j, backward, N)
      # black square, so either flip both or flip none
      if board[i][j] == BLACK:
        # not(xor(d, d2)) can be encoded by separating them with a dummy node
        dummy = ct
        ct += 1
        xor(d, dummy)
        xor(dummy, d2)
      # white square, so must flip exactly one (xor)
      else:
        xor(d, d2)
  return bipartite(g, num_diag)

if __name__ == "__main__":
  read_input()