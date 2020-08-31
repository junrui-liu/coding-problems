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
