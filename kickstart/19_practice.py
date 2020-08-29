from itertools import islice
from pprint import pprint

def mural(ns):
  m = (len(ns) + 1) // 2
  s = sum(islice(ns, 0, m))
  i = 0
  max_score = s
  for j in range(m, len(ns)):
    s = s + ns[j] - ns[i]
    if s > max_score:
      max_score = s
    i += 1
  return max_score

def mural_main():
  T = int(input())
  for t in range(1,T+1):
    _ = input()
    ns = [int(c) for c in input()]
    res = mural(ns)
    print("Case #{}: {}".format(t, res))

def alarm(ns, k):
  import itertools
  M = 1000000007

  def geo_sum(r,k):
    return (r**(k+1) - r) // (r-1)

  length = len(ns)
  s = 0
  prev = 0
  for i in range(length-1, -1, -1): # from length-1 down to 0
    prev = ((prev + ns[i] * (length - i))) % M
    print(i, prev)
    s += prev * geo_sum(i+1,k)
  return s % M

def alarm_naive(ns,k):
  def dot(xs, ys):
    return sum(x * y for x,y in zip(xs, ys))
  s = 0
  for ki in range(1,k+1):
    for i in range(len(ns)):
      for j in range(i, len(ns)):
        v = [b**ki for b in range(1,j-i+2)]
        s += dot(ns[i:j+1], v)
  return s % 1000000007

def alarm_main():
  t = int(input())
  for ti in range(1,t+1):
    N,K,x1,y1,C,D,E1,E2,F = [int(c) for c in input().split()]
    _x, _y = x1, y1
    ns = []
    for i in range(N):
      ns.append((_x+_y) % F)
      _x, _y = (C * _x + D * _y + E1) % F, (D * _x + C * _y + E2) % F
    print("Case #{}: {}".format(ti, alarm(ns,K)))

if __name__ == "__main__":
  alarm_main()
  # print(alarm(
  # ns,k = [0,1,2],1
  # ns,k=[20003, 9173, 88207, 28796, 62914, 80382, 58863, 2636, 87393, 80057],10
  # print(alarm_naive(ns,k), alarm(ns,k))
