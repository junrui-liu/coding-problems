from __future__ import print_function
import random

if hasattr(__builtins__, 'raw_input'):
    input = raw_input

def read_ints():
  return [int(x) for x in input().split()]

def read_int():
  return int(input())

def choices(seq, k=1):
  return [random.choice(seq) for _ in range(k)]


def allocation(A, B):
  A.sort()
  count = 0
  i = 0
  while B > 0 and i < len(A) and A[i] <= B:
    count += 1
    B -= A[i]
    i += 1
  return count
    


def allocation_main():
  T = read_int()
  for t in range(T):
    N, B = read_ints()
    A = read_ints()
    print('Case #{}: {}'.format(t+1,allocation(A, B)))

def plates_rec(N,K,P,A):
  def rec(p,n,k):
    res = 0
    if p <= 0 or n <= 0 or k > K:
      res = 0
    elif K-k+1 + (n-1)*K < p: # not enough plates remain
      res = 0
    elif cache[p][n][k] is not None:
      res = cache[p][n][k]
    else:
      r1 = rec(p,n-1,1) # don't use this stack
      r2 = rec(p-1,n-1,1) + A[n-1][k-1] # use stack top
      r3 = rec(p-1,n,k+1) + A[n-1][k-1] # use more than stack top
      res = max(r1,r2,r3)
    cache[p][n][k] = res
    return res    
  return rec(P,N,1)


def plates(N,K,P,A):
  B = [[None for n in range(N)] for p in range(P+1)]
  # No plates
  for n in range(N):
    B[0][n] = 0
  # >= 1 plate
  s = 0
  for k in range(min(K,P)):
    s += A[0][k]
    B[k+1][0] = s
  
  for n in range(1,N):
    for p in range(1,P+1):
      m = B[p][n-1]
      stack_beauty = 0
      for k in range(min(K,p)):
        beauty = A[n][k]
        stack_beauty += beauty
        prev_ind = (p-k-1,n-1)
        prev = B[p-k-1][n-1]
        if prev is None:
          continue
        candidate = prev + stack_beauty
        if m is None or candidate > m:
          m = candidate
      B[p][n] = m
  return B[P][N-1]

def plates_main():
  T = read_int()
  for t in range(1,T+1):
    N,K,P = read_ints()
    A = []
    for _ in range(N):
      A.append(read_ints())
    res = plates(N,K,P,A)
    print('Case #{}: {}'.format(t, res))

def bin_search(xs, comparator):
  lo = 0
  hi = len(xs)-1
  while True:
    mid = (hi + lo) // 2
    compare = comparator(xs, mid)
    if compare == 0:
      return mid, None, None
    if compare < 0:
      hi = mid - 1
    elif compare > 0:
      lo = mid + 1
    if lo > hi:
      return None, hi, lo

def workout(M, K):
  intervals = [M[i]-M[i-1] for i in range(1,len(M))]
  intervals.sort(reverse=True)
  def comparator(intervals, j):
    from math import ceil
    cover = intervals[j]
    count = 0
    i = 0
    while count <= K and i < j:
      to_cover = intervals[i]
      count += ceil(to_cover / cover)-1
    if count > K and i < j:
      return -1
    elif count <= K and i >= j:
      return 1
    else:
      return 0
  i, lo, hi = bin_search(intervals, comparator)
  if i is not None:
    return intervals[i]
  # not enough K to cover
  elif lo < 0:
    assert(hi == 0)
    interval = intervals[hi]
    return max(interval // K, interval % K)
  # more than enough K
  elif hi >= len(M):
    assert(lo == len(M)-1)
    interval = intervals[lo]
    return -1
    # need to use binary search to find the exact interval? (no upper bound?)
  else:
    return intervals[hi]

def workout_inspired(M,K):
  from math import ceil
  intervals = []
  d_max = 0
  for i in range(1,len(M)):
    intv = M[i]-M[i-1]
    intervals.append(intv)
    if intv > d_max:
      d_max = intv
  d_min = 1
  lo, hi = d_min, d_max
  def covers(M, d):
    count = 0
    i = 0
    while count <= K and i < len(intervals): 
      to_cover = intervals[i]
      count += ceil(to_cover / mid)-1
      i += 1
    return count <= K
  d_feasible = d_max
  while lo <= hi:
    mid = (lo + hi) // 2
    if covers(intervals, mid):
      hi = mid - 1
      d_feasible = mid
    else:
      lo = mid + 1
  return d_feasible


def workout_main():
  T = read_int()
  for t in range(1,T+1):
    N,K = read_ints()
    M = read_ints()
    res = workout_inspired(M, K)
    print('Case #{}: {}'.format(t, res))


NUL = ''

# type ann_tree = (tree, size: int, depth: int, deepest: int)
# type tree = Leaf | Node of char * (ann_tree list)

def group_copy(ss):
  from collections import defaultdict
  groups = defaultdict(list)
  for s in ss:
    hd = s[0] if len(s) > 0 else NUL
    groups[hd].append(s[1:])
  return groups

def build_prefix_tree_rec(ss): # type: string list -> ann_tree
  groups = group_copy(ss)
  size = 0
  depth = -1
  deepest = None
  children = [] # type: ann_tree
  for i, (hd,tls) in enumerate(groups.items()):
    if hd != NUL:
      subtree, subsize, subdepth, subdeepest = build_prefix_tree_rec(tls) # subtree: tree
      subtree[0] = hd + subtree[0] # subtree cannot be a leaf
    else:
      subtree, subsize, subdepth, subdeepest = NUL, len(tls), 0, None
    children.append((subtree, subsize, subdepth, subdeepest))
    size += subsize
    if subdepth > depth:
      depth = subdepth
      deepest = i
  
  if len(groups) == 1 and hd != NUL:
    return subtree, size, depth, subdeepest
  else:
    return ([NUL, children], size, depth+1, deepest)

def longest(ann_tree):
  tree, size, depth, deepest = ann_tree
  if tree == NUL:
    return ''
  hd, children = tree
  return hd + longest(children[deepest])

class Stack:
  def __init__(self):
    self.s = []
  def push(self, x):
    self.s.append(x)
  def pop(self):
    return self.s.pop()
  def empty(self):
    return len(self.s) == 0

import heapq as hq
class PQueue:
  def __init__(self):
    self.q = []
  def put(self, priority, x):
    hq.heappush(self.q, (priority, x))
  def get(self):
    return hq.heappop(self.q)
  def empty(self):
    return len(self.q) == 0
  def peek(self):
    return self.q[0]

from functools import total_ordering
@total_ordering
class PTree:
  counter = 0
  NUL = ''
  FMT = '{id:>3}  {prefix:>12}  {string:>12}  {children}'
  T_LEAF = 0
  T_NODE = 1
  def __init__(self, type, prefix=NUL, parent=None):
    self.prefix = prefix
    self.parent = parent
    self.children = []
    self.id = PTree.counter
    self.offset = None
    self.string = ''
    PTree.counter += 1
  
  def __lt__(self, other):
    return self.id < other.id 
  
  def __eq__(self, other):
    return self.id == other.id
  
  def to_str(self):
    ch = self.prefix if self.prefix!= PTree.NUL else '/'
    s = PTree.FMT.format(id=self.id, prefix=ch, string=self.string,
       children=[child.id for child in self.children])
    L = [s]
    for child in self.children:
      L += child.to_str()
    return L
  
  def __str__(self):
    header = PTree.FMT.format(id='id', prefix='ch', string='str', children='children')
    return '\n'.join([header] + self.to_str())
  
  def destruct(self):
    if self.children == []:
      return [self.ch]
    L = []
    for child in self.children:
      L += [self.prefix+ e for e in child.destruct()]
    return L

  def max_witness(xs):
    from itertools import islice
    xs = iter(xs)
    maxi = next(xs)
    witness = 0
    for i,x in enumerate(xs):
      if x > maxi:
        maxi = x
        witness = i+1
    return maxi, witness

  @staticmethod
  def group(ss, indices, level):
    from collections import defaultdict
    groups = defaultdict(list)
    for i in indices:
      s = ss[i]
      hd = s[level] if level < len(s) else NUL
      groups[hd].append(i)
    return groups
  
  @staticmethod
  def construct(ss):
    queue = PQueue()
    stack = Stack()
    level = 0
    root = PTree(PTree.T_NODE, parent=None)
    stack.push((root, [i for i in range(len(ss))], level, -1))
    height = 0
    while not stack.empty():
      node, indices, level, ngroups = stack.pop()
      if indices is not None: # First encounter
        groups = PTree.group(ss, indices, level)
        # Visit this node again after its children are processed
        stack.push((node, None, level, len(groups)))
        for (ch,ch_indices) in groups.items():
          children = []
          if ch == PTree.NUL:
            for i in range(len(ch_indices)):
              child = PTree(PTree.T_LEAF, parent=node)
              children.append(child)
          else:
            child = PTree(PTree.T_NODE, prefix=ch, parent=node)
            stack.push((child, ch_indices, level+1, -1))
            children.append(child)
          for child in children:
            child.string = node.string + ch # DELETE
            child.offset = len(node.children) # reverse pointer
            node.children.append(child)
      else: # Second encounter
        height = max(level, height)
        if len(node.children) == 1:
          child = node.children[0]
          child.parent = node.parent
          child.offset = node.offset
          child.prefix= node.prefix+ child.prefix# DELETE
          if node.parent:
            node.parent.children[node.offset] = child
        else:
          queue.put(-level, node)
    return root, queue, height


def bundling(ss, K):
  t, q, h = PTree.construct(ss)
  score = 0
  # Start at the second deepest level
  while not q.empty():
    level, node = q.get()
    d = -level
    s = node.string
    num_child = sum(1 if child else 0 for child in node.children)
    score += (num_child // K) * d
    # push leftover children up a level
    num_left = num_child % K
    if num_left != 1 and node.parent:
        node.parent.children += [True for _ in range(num_child - num_left)]
        node.parent.children[node.offset] = None
  return score

# t,q,h = PTree.construct(['a', 'a'])
# bundling(['a', 'a'], 2)
# t,q,h = PTree.construct(['RAINBOW', 'FIREBALL', 'RANK', 'RANDOM', 'FIREWALL', 'FIREFIGHTER', 'ALLOCATION', 'PLATE', 'WORKOUT', 'BUNDLING'])
# bundling(['RAINBOW', 'FIREBALL', 'RANK', 'RANDOM', 'FIREWALL', 'FIREFIGHTER', 'ALLOCATION', 'PLATE', 'WORKOUT', 'BUNDLING'], 3)
bundling(['RAINBOW', 'FIREBALL', 'RANK', 'RANDOM', 'FIREWALL', 'FIREFIGHTER'], 3)

def bundling_main():
  T = read_int()
  for t in range(1,T+1):
    N,K = read_ints()
    ss = []
    for _ in range(N):
      ss.append(input().rstrip())
    res = bundling(ss, K)
    print('Case #{}: {}'.format(t, res))

def bundling_rand_test():
  N = 10**5
  K = 10**2
  alpha = [chr(ord('A')+i) for i in range(26)]
  ss = []
  for _ in range(N):
    ss.append(''.join(choices(alpha, k=5)))
  print("start")
  bundling(ss, K)

# bundling_rand_test()
# if __name__ == '__main__':
  # bundling_main()
  
  # workout_main()
  # plates_main()
  # print(plates(2,4,5,[[10,10,100,30],[80,50,10,50]]))
  # print(plates(3,2,3,[[80,80],[15,50],[20,10]]))
  # print(plates(3,2,7,[[80,80],[15,50],[20,10]]))