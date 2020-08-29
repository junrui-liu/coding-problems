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
    N, M = read_ints()
    xs = read_int_arr()
    res = solve(xs, M)
    print("Case #{}: {}".format(t, res))

# Solution begins here
def solve(xs, M):
  lo = 0
  hi = None
  test = lambda k: sum((x^k for x in xs)) <= M
  # find upper bound
  while hi is None:
    print(lo)
    if test(2 * lo):
      lo = lo * 2 if lo 
    else:
      hi = 2 * lo
  # binary search
  while lo + 1 < hi:
    mid = (lo + hi) // 2
    print(lo,hi,mid)
    if test(mid):
      lo = mid
    else:
      hi = mid
  
  return lo+1 if test(lo+1) else -1

if __name__ == "__main__":
  read_input()