def Cr(n,k):
  num = 1
  den = 1
  for _ in range(k):
    num *= n
    den *= k
    n -= 1
    k -= 1
  return num // den
def count_seq(j,k):
  if k >= 0 and j-k >= 0:
    return Cr(j,j-k) * 9**k
  else:
    return 0

def min_with_len(k):
  return 10**(k-1) # 10..0

def max_with_len(k):
  return min_with_len(k+1) - 1 # 99..9

def explode(x):
  if x == 0: return [0]
  l = []
  while x > 0:
    l.append(x % 10)
    x //= 10
  return l[::-1]

def count_min_to_upper(ub, k):
  """Given an upper bound with len l, count ints in [10**l, ub] with k non-zero digits"""
  def rec(ub, k, acc):
    l = len(ub)
    if l == 0:
      if k == 0: return acc+1
      else: return acc
    if l < k: return acc
    if ub[0] == 0:
      return rec(ub[1:], k, acc)
    ub_hi_set = [ub[i] if i == 0 else 0 for i in range(l)]
    count_lower = count_seq(l-1, k) + (ub[0]-1) * count_seq(l-1,k-1)
    return rec(ub[1:], k-1, acc + count_lower)
  if ub[0] == 1:
    return rec(ub[1:], k-1, 0)
  else:
    lower = (ub[0]-1) * count_seq(len(ub)-1, k-1)
    return lower + rec(ub[1:], k-1, 0)

def implode(digits):
  x = 0
  l = len(digits)
  for i in range(l):
    x = x * 10 + digits[i]
  return x

def count_min_to_upper2(ub, k):
  lb = [1 if i == 0 else 0 for i in range(len(ub))]
  lb_x = implode(lb)
  ub_x = implode(ub)
  count = 0
  for x in range(lb_x, ub_x+1):
    if sum((1 if d > 0 else 0 for d in explode(x))) == k:
      count += 1
  return count


def number_of_integers(l, r, k):
  l += 1
  # count the number of sequences {0,1,...,9}^j containing j-k zeros
  total = 0
  l_list, r_list = explode(l), explode(r)
  l_hi, l_len = l_list[0], len(l_list)
  r_hi, r_len = r_list[0], len(r_list)
  # iteratively count ints in [l, r_len-1]
  # 0 subtract count of ints in [10..0, l-1]
  i = l_len
  if l > min_with_len(i):
    total -= count_min_to_upper(explode(l-1), k)
  while i != r_len:
    # the highest (i-th) digit \in {1..9} uses 1 non-zero, so the remaining (i-1) sequence can have k-1
    total += 9 * count_seq(i-1, k-1)
    i += 1
  # now count ints in [10^r_len, r]
  total += count_min_to_upper(r_list, k)
  return total % (10**9+7)

class Heap():
  @staticmethod
  def parent(i): return i//2
  @staticmethod
  def sibling(i): return i^1
  @staticmethod
  def left(i): return 2*i
  @staticmethod
  def right(i): return 2*i + 1
  @staticmethod
  def key(kv): return kv[0]
  @staticmethod
  def val(kv): return kv[1]
  @staticmethod
  def compare(kx, ky): return Heap.key(kx) - Heap.key(ky)

  def __init__(self, keys=[], vals=[], debug=False):
    assert(len(keys) == len(vals))
    self.initialized = False
    self.a = [None]
    self.size = 0
    self.d = dict()
    for k,v in zip(keys, vals):
      self.insert(v, k, rise=False)
    self.heapify()
    self.initialized = True
    self.debug = debug
    # self.check([self.heap_property, self.repr_invariant])
  
  def is_valid(self, i):
    return i >= 1 and i <= self.size

  def key_at(self, i):
    return Heap.key(self.a[i])
  
  def val_at(self, i):
    return Heap.val(self.a[i])

  def find(self, v):
    return self.d[v]

  def update_key(self, i, new_k):
    assert(self.is_valid(i))
    # self.check([self.repr_invariant]) # RI
    old_k, vi = self.key_at(i), self.val_at(i)
    self.a[i] = (new_k, vi)
    # self.check([self.repr_invariant]) # RI
  
  def swap(self, i, j):
    assert(self.is_valid(i) and self.is_valid(j))
    # self.check([self.repr_invariant]) # RI
    vi, vj = self.val_at(i), self.val_at(j)
    self.a[i], self.a[j] = self.a[j], self.a[i]
    self.d[vi], self.d[vj] = j, i
    # self.check([self.repr_invariant]) # RI
  
  def remove(self, i):
    assert(self.is_valid(i))
    # self.check([self.repr_invariant]) # RI
    vi = self.val_at(i)
    self.a[i] = None
    del self.d[vi]
    self.size -= 1
    # self.check([self.repr_invariant]) # RI
    return vi

  def insert(self, v, k=None, rise=True):
    if v in self.d: # values must be distinct
      raise ValueError("Values must be distinct")
    if k is None: k = v # use value as key if key is not supplied
    self.size += 1 # new (k,v) will go here
    if self.size == len(self.a):
      self.a.append( (k,v) )
    else:
      self.a[self.size] = (k,v)
    self.d[v] = self.size
    if rise:
      self.rise(self.size)
    # self.check([self.heap_property, self.repr_invariant])
  
  def restore(self, ip):
    # self.check([self.repr_invariant]) # RI
    i_child = None # which child is swapped with parent
    il, ir = Heap.left(ip), Heap.right(ip)
    if self.is_valid(ir): # has right (& left) child
        p, l, r = self.a[ip], self.a[il], self.a[ir]
        if Heap.compare(p, l) > 0 or Heap.compare(p, r) > 0: # heap property violated
          if Heap.compare(l, r) > 0:
            i_child, child = ir, r
          else:
            i_child, child = il, l
    elif self.is_valid(il): # has left child
      p, l = self.a[ip], self.a[il]
      if Heap.compare(p, l) > 0:
        i_child, child = il, l
    if i_child is not None:
      self.swap(ip, i_child)
    # self.check([self.repr_invariant]) # RI
    # self.check_local(ip, self.heap_property)
    return i_child

  def heap_property(self, ip):
    maintained = True
    if self.is_valid(ip):
      il, ir = Heap.left(ip), Heap.right(ip)
      if self.is_valid(il):
        maintained &= self.key_at(ip) <= self.key_at(il)
      if self.is_valid(ir):
        maintained &= self.key_at(ip) <= self.key_at(ir)
    return maintained
  heap_property.name = "HEAP"
  
  def repr_invariant(self, i):
    vi = self.val_at(i)
    # return vi in self.d and self.d[vi] == i
    return self.d[vi] == i
  repr_invariant.name = "RI"
  
  def check_local(self, i, property):
    if not (self.initialized and self.debug): return
    assert(property(i))

  def check(self, properties):
    if not (self.initialized and self.debug): return
    for i in range(self.size, 0, -1):
      for j, p in  enumerate(properties):
        if not p(i):
          print("Property {} violated at {}".format(p.name, i))
          assert(p(i))

  def heapify(self):
    for i in range(self.size // 2, 0, -1):
      self.sink(i)
    # self.check([self.heap_property, self.repr_invariant])

  def sink(self, i):
    count = 0
    while self.is_valid(i):
      i = self.restore(i)
      if i is None: break
      count += 1
    # self.check([self.heap_property, self.repr_invariant])
  
  def rise(self, i):
    i = Heap.parent(i)
    count = 0
    while self.is_valid(i):
      if self.restore(i) is None: break
      i = Heap.parent(i)
      count += 1
    # self.check([self.heap_property, self.repr_invariant])
  
  def decrease_key(self, v, new_k):
    # self.check([self.heap_property, self.repr_invariant])
    i = self.find(v)
    if self.key_at(i) <= new_k: return # do nothing if new key is not smaller
    self.update_key(i, new_k)
    self.rise(i)
    # self.check([self.heap_property, self.repr_invariant])
  
  def increase_key(self, v, new_k):
    # self.check([self.heap_property, self.repr_invariant])
    i = self.find(v)
    if self.key_at(i) >= new_k: return # do nothing if new key is not larger
    self.update_key(i, new_k)
    self.sink(i)
    # self.check([self.heap_property, self.repr_invariant])

  def priority_of(self, v):
    i = self.find(v)
    return Heap.key(self.a[i])

  def extract_min(self):
    # self.check([self.heap_property, self.repr_invariant])
    m = self.a[1]
    res = self.key_at(1), self.val_at(1)
    if self.size > 0:
      self.swap(1, self.size)
      self.remove(self.size)
      self.sink(1)
    # self.check([self.heap_property, self.repr_invariant])
    return res
  
  def toggle_debug(self, flag):
    self.debug = flag
  
  @staticmethod
  def heapsort(xs):
    h = Heap(xs, xs)
    l = []
    while h.size > 0:
      l.append(h.extract_min()[0])
    return h, l

  @staticmethod
  def random_test():
    import random
    L = 10**5
    l = list(set(random.choices(list(range(L)),k=L//2)))
    h = Heap(l, l, debug=False)
    h.toggle_debug(True)
    s = set(l)
    for t in range(L):
      i = random.randint(1,h.size)
      k = h.priority_of(h.a[i][1])
      r = random.random()
      if r*3 < 1: # increase
        h.increase_key(h.a[i][1], random.randint(k, L))
      elif r*3 < 2:
        h.decrease_key(h.a[i][1], random.randint(0, k))
      else:
        x = h.extract_min()

def optimal_network_routing(cost):
  import math, itertools
  import queue
  R, C = len(cost), len(cost[0])
  
  h = Heap()
  make_grid = lambda x: [[x for j in range(C)] for i in range(R)]
  score = make_grid(math.inf)
  def is_valid(i,j):
    return i >= 0 and i < R and j >=0 and j < C
  def processed(i,j):
    return score[i][j] < math.inf
  for i in range(R):
    for j in range(C):
      if i == 0 and j == 0:
        h.insert((0,0), 0)
      else:
        h.insert((i,j), math.inf)
  
  while h.size > 0:
    key, (ai, aj) = h.extract_min()
    score[ai][aj] = key
    cost_0 = cost[ai][aj]
    # relax every crossing edge from (ai,aj) to its neighbors
    for di, dj in [(1,0),(-1,0),(0,1),(0,-1)]:
      bi, bj = ai + di, aj + dj
      if is_valid(bi,bj) and not processed(bi,bj):
        cost_0to1 = abs(cost[ai][aj] - cost[bi][bj])
        cost_1 = max(key, cost_0to1)
        h.decrease_key((bi,bj), cost_1)
  return score[-1][-1]