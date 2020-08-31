def array_sum_operation(n, ops):
  xs = [i+1 for i in range(n)]
  elems = set()
  total = (1+n)*n//2
  res = list()
  for op in ops:
    if op in elems:
      xs[0], xs[-1] = xs[-1], xs[0]
      res.append(total)
    else:
      total = total - xs[-1] + op
      res.append(total)
      elems.remove(xs[-1])
      elems.add(op)
      xs[-1] = op
  return res

def construct_tree(n,x):
  n -= 1 # don't count the root
  if n == 0 and x == 0:
    return []
  # An (n,x) tree is possible if and only if n <= x (all nodes have depth 1)
  # and n*(n+1)//2 >= x (linear path with total depths = arithmetic sum 1...n)
  if n > x or n*(n+1)//2 < x:
    return [(-1,-1)]
  # Otherwise, every tree of (n,x) is achievable
  # To see this, start with the lowest-score tree (n,n), where all nodes have depth 1.
  # Promote a node from depth 1 to 2 increases the score by 1.
  # Do this for n-1 nodes, and we filled level 2.
  # Repeatedly promote nodes and fill each level until we reach a score of x.
  
  # A [filled tree] has a linear path with k-1 nodes, and a flat bush with n-(k-1) nodes at depth k
  filled_score = lambda k: k*(k-1)//2 + k*(n-k+1)

  def direction(k):
    if x > filled_score(k):
      return 1
    elif x <= filled_score(k-1):
      return -1
    else:
      return 0

  lo = 1
  hi = n
  while lo < hi:
    mid = (lo + hi) // 2
    d = direction(mid)
    if d > 0:
      lo = mid + 1
    elif d < 0:
      hi = mid - 1
    else:
      lo, hi = mid, mid
  assert(lo == hi)
  k = lo # current level
  prev_filled_score = filled_score(k-1) if k > 0 else 0
  res = list()
  count = 1
  n_linear = max(0, k-2) # number of linear nodes of depths 0, 1, ..., k-1
  n_current = max(0, x - filled_score(k-1)) # partially fill level k
  n_prev = max(0, n - n_linear - n_current) # the remaining nodes partially fill level k-1
  # Output the edges
  count = 1
  for _ in range(n_linear):
    res.append(( count-1, count ))
    count += 1
  for _ in range(n_prev):
    res.append(( k-2, count ))
    count += 1
  for i in range(n_current):
    res.append(( k-1, count ))
    count += 1
  return list(map(lambda p: (p[0]+1,p[1]+1), res))

def solving_for_queries_with_cups(n, balls, swaps, queries):
  # print(n, balls, swaps, queries)
  balls = set(map(lambda i:i-1, balls))
  for i,j in swaps:
    i, j = i-1, j-1
    # if cup x contains a ball and cup y doesn't,
    # then remove x from the set and add y to it
    if i in balls and j not in balls:
      balls.remove(i)
      balls.add(j)
    elif j in balls and i not in balls:
      balls.remove(j)
      balls.add(i)

  def binary_search(L, R, check):
    lo, hi = L, R
    # Invariant: lo < min pos that passes check, hi > max pos that passes check
    while lo +1 < hi:
      mid = (lo + hi) // 2
      # at least one between lo and hi, so L <= lo < mid < hi <= R
      c = check(mid)
      if c > 0:
        lo = mid
      elif c < 0:
        hi = mid
      else:
        return mid-1, mid+1 # lo +2 == mid +1 == hi, where mid passes check
    # loop breaks only when lo +1 == hi
    return lo, hi

  balls = list(balls)
  balls.sort()
  B = len(balls)
  res = list()
  for l,r in queries:
    l, r = l-1, r-1
    i_lo, i_hi = binary_search(-1, B, lambda i: l-balls[i])
    # i_lo is the maximum index that fails the check, so i_lo+1 passes if it's valid
    i = i_lo +1
    j_lo, j_hi = binary_search(-1, B, lambda i: r-balls[i])
    # j_hi is the minimum index that fails the check, so j_hi-1 passes if it's valid
    j = j_hi -1
    if i >= B or j < 0: # requested interval contains no ball
      res.append(0)
    else:
      i, j = max(i, 0), min(B-1, j)
      res.append(j-i+1)
  return res

class UF:
  def __init__(self, n):
    self.n = n # total number of elements
    self.p = list(range(n)) # parent
    self.s = [1 for _ in range(n)] # subtree size
  def is_root(self, i):
    return self.p[i] == i
  def find(self, i):
    parent = self.p[i]
    if parent == i:
      return i
    r = self.find(parent)
    self.p[i] = r
    return r
  def union(self, i, j):
    ri, rj = self.find(i), self.find(j)
    if ri == rj: return
    if self.s[ri] < self.s[rj]:
      smaller, larger = ri, rj
    else:
      smaller, larger = rj, ri
    self.p[smaller] = larger
    self.s[larger] += self.s[smaller]
  def connected(self, i, j):
    return self.find(i) == self.find(j)
  def num_components(self):
    return sum( (1 for i in range(self.n) if self.is_root(i)) )
  def components(self):
    return [ i for i in range(self.n) if self.is_root(i) ]
  def depth(self, i):
    count = 0
    while self.p[i] != i:
      i = self.p[i]
      count += 1
    return count
  def all_depth(self):
    return [self.depth(i) for i in range(self.n)]
  def random_test(self):
    N = int(1e6)
    import random; randi = lambda: random.randint(0,N-1)
    import itertools; argmax = lambda l: max(zip(itertools.count(), l),key=lambda p:p[1])[0]
    u = UF(N)
    for _ in range(int(1e5)):
      i,j = randi(), randi()
      u.union(i,j)
    return u

def rerouting(connections):
  # First attempt using union-find
  # from collections import defaultdict
  # # Auxillary structures
  # n = len(connections)
  # uf = UF(n)
  # for u,v in enumerate(connections):
  #   v -= 1
  #   uf.union(u,v)
  # families = 0
  # singletons = 0
  # for i in range(n):
  #   if uf.is_root(i):
  #     if uf.s[i] > 1:
  #       families += 1
  #     else:
  #       singletons += 1
  # if singletons > 0:
  #   return families + (singletons - 1)
  # else:
  #   return families

  # Second attempt using DFS
  from collections import defaultdict
  def next_hop(i):
    return connections[i]-1
  cycles_multi = 0
  cycles_single = 0
  n = len(connections)
  visited = [False for _ in range(n)]
  ids = [-1 for _ in range(n)]
  for i in range(n):
    j = i
    while not visited[j]:
      visited[j] = True
      ids[j] = i # j is in i's component
      j = next_hop(j)
    if ids[j] == i: # new cycle on the current dfs path
      if next_hop(j) == j:
        cycles_single += 1
      else:
        cycles_multi += 1
    # else we found a visited route (cycle)    
  if cycles_single > 0:
    return cycles_multi + cycles_single -1
  else:
    return cycles_multi

class DLList:
  class Node:
    def __init__(self, v):
      self.v = v
      self.prev = None
      self.next = None
    
  def __init__(self):
    self.first = None
    self.last = None
  
  def append(self, v):
    node = self.Node(v)
    if self.first is None:
      self.first, self.last = node, node
    else:
      before = self.last
      before.next = node
      node.prev = before
      self.last = node
    return node
  
  def insert_after(self, before, v):
    node = self.Node(v)
    if before.next is not None:
      before.next.prev = node
      node.next = before.next
    before.next = node
    node.prev = before
    if self.last == before:
      self.last = node
    return node
  
  def delete(self, node):
    if self.first == node:
      self.first = node.next
    if self.last == node:
      self.last = node.prev
    if node.prev is not None:
      node.prev.next = node.next
    if node.next is not None:
      node.next.prev = node.prev


def new_keyboard(cmds):
  l = DLList()
  sof_ch = "/" # start-of-file
  sof = l.append("/")
  cursor = sof
  num_lock = True
  def print_state(l, cursor):
    p = l.first
    while p is not None:
      print(p.v, end="")
      if p == cursor:
        print("[>>]", end="")
      p = p.next
    print()
  for cmd in cmds:
    if cmd == "<":
      cursor = sof
    elif cmd == ">":
      cursor = l.last
    elif cmd == "*" and cursor != sof:
      prev = cursor.prev
      l.delete(cursor)
      cursor = prev
    elif cmd == "#":
      num_lock = not num_lock
    elif not cmd.isnumeric() or num_lock:
      cursor = l.insert_after(cursor, cmd)
    # print_state(l,cursor)
  res = list()
  p = l.first.next
  while p is not None:
    res.append(p.v)
    p = p.next
  return "".join(res)
# new_keyboard("HE*<LL>O")
