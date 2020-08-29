
def eea(a,b):
  ro, r = max(a,b), min(a,b) # o for old
  so, s = (1, 0)
  to, t = (0, 1)
  while r > 0:
    q = ro // r
    ro, r = r, ro - q*r
    so, s = s, so - q*s
    to, t = t, to - q*t
  return (ro, s, t)

def solve_case(A, B, p_a, p_b):
  """Solve the case for Amadea starting at p_a with speed A,
  and Bilva starting at p_b with speed B"""
  a = p_a - p_a // A
  b = p_b - p_b // B
  # We have sequences {Ax + a} and {By + b}
  # Solve diophantine equation Ax + a = By + b, i.e. Ax - By = b - a := C
  # using extended Euclidean algorithm
  C = b - a
  gcd, x, y = eea(A, B)
  # No solution if C does not divide gcd(A,B)
  if C % gcd != 0: return 0 
  lcm = A * B / gcd


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
    length, a, b = read_ints()
    parents = read_int_arr()
    res = solve(a, b, parents)
    print("Case #{}: {}".format(t, res))


def solve(a, b, parents):
  for i in range(len(parents)):
    parents[i] -= 1
  # print(parents)

  def parent_of(i):
    return parents[i-1]

  def rise(i, d):
    assert(d > 0)
    _i, _d = i, d
    while d > 0:
      i = parent_of(i)
      d -= 1
    # print("(+{}) {} -> {}".format(_d,_i,i))
    return i

  from heapq import heappush, heappop
  from itertools import islice
  N = len(parents)+1
  depth = [0 for _ in range(N)]
  ct_a = [0 for _ in range(N)]
  ct_b = [0 for _ in range(N)]
  q = []
  heappush(q, (0, 0))
  for i, p in enumerate(parents):
    i += 1 # parents array start from node 1, not 0
    # p -= 1 # input uses 1-index array
    depth[i] = depth[p] + 1
    # use minus depth as priority
    heappush(q, (-depth[i], i))
  while len(q) > 0:
    d, i = heappop(q)
    d = -d
    # print("i", i, "d", d)
    ct_a[i] += 1
    ct_b[i] += 1
    if d >= a:
      ct_a[rise(i, a)] += ct_a[i]
      # print("A:", ct_a)
    if d >= b:
      ct_b[rise(i, b)] += ct_b[i]
      # print("B:", ct_b)
  # print([i for i in range(N)])
  # print(ct_a)
  # print(ct_b)
  
  # Compute total beauty
  total = 0
  for i in range(N):
    x, y = ct_a[i], ct_b[i]
    total += (x+y) * N - x*y
  return total / (N**2.0)

  
# print(solve(2,3, [1, 1, 3, 4, 4, 3, 4]))
if __name__ == "__main__":
  read_input()