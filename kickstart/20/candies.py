#!/usr/bin/env python3
from math import ceil, log2
import itertools

UPDATE = 'U'
QUERY = 'Q'

def read_ints():
  return [int(i) for i in input().split()]

def read_int_arr():
  return list(map(int, input().split()))

def parse_query(line):
  op, x, y = line.split()
  return op, int(x), int(y)

def read_input():
  num_cases = int(input())
  for t in range(1, num_cases+1):
    total = 0
    N, Q = read_ints()
    xs = read_int_arr()
    qs = [input() for _ in range(Q)]
    res = solve(xs, qs)
    print("Case #{}: {}".format(t, res))

def solve_naive(xs, qs):
  total = 0
  for qi, q in enumerate(qs):
    op, arg1, arg2 = parse_query(q)
    if op == UPDATE:
      xs[arg1-1] = arg2
    elif op == QUERY:
      q_sum = 0
      for i in range(arg2-arg1+1):
        multiplier = i + 1
        scalar = (-1 if multiplier % 2 == 0 else 1) * multiplier
        q_sum += scalar * xs[arg1+i-1]
      total += q_sum
  return total

class SegmentTree:
  
  def __init__(self, xs):
    self.n = int( 2 ** ceil(log2(len(xs))) )
    self.t = [ 0 for _ in range(self.n * 2) ]
    for i in range(len(xs)):
      self.t[ self.n + i ] = xs[ i ]
    for i in range(self.n-1, 0, -1):
      self.t[ i ] = self.t[ 2*i ] + self.t[ 2*i + 1 ]
  
  def modify(self, i, val):
    i += self.n
    self.t[ i ] = val
    while i > 1:
      # print(i, i//2, i^1)
      self.t[ i//2 ] = self.t[ i ] + self.t[ i^1 ]
      # print(self.t[ i//2 ])
      i //= 2
  
  def get(self, i):
    return self.t[ self.n + i ]

  def query(self, l, r):
    l += self.n
    r += self.n
    res = 0
    while l < r:
      if l & 1: # l odd
        res += self.t[ l ]
        l += 1
      if r & 1: # r odd
        r -= 1
        res += self.t[ r ]
      l = l // 2
      r = r // 2
    return res

l = list(range(10))
st = SegmentTree(l)

def seq(a0, f=lambda x: x):
  while True:
    yield a0
    a0 = f(a0)

def geometric(a0, k=1):
  return seq(a0, lambda x: k * x)

def arithmetic(a0, d=0):
  return seq(a0, lambda x: x + d)

def solve(xs, qs):
  total = 0
  mult = lambda p: p[0] * p[1]
  a = list(map(mult, zip(geometric(1, k=-1), xs)))
  m = list(map(mult, zip(arithmetic(1, d=1), a)))
  t_a = SegmentTree(a)
  t_m = SegmentTree(m)
  for qi, q in enumerate(qs):
    op, arg1, arg2 = parse_query(q)
    if op == UPDATE:
      i, val = arg1 - 1, arg2
      sign = (-1)**i
      t_a.modify(i, val * sign )
      t_m.modify(i, val * sign * (i+1))
    elif op == QUERY:
      l, r = arg1 - 1, arg2
      m_r = t_m.query(0, r) 
      m_l = t_m.query(0, l)
      a_lr = t_a.query(l,r)
      res = m_r - m_l - l * a_lr
      if l % 2 == 1:
        res *= -1
      total += res
  return total

if __name__ == "__main__":
  read_input()