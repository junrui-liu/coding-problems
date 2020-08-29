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

NUL = ''

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
  def put(self, priority_x):
    hq.heappush(self.q, priority_x)
  def get(self):
    return hq.heappop(self.q)
  def empty(self):
    return len(self.q) == 0
  def peek(self):
    return self.q[0]


from functools import total_ordering
@total_ordering
class Trie:
  counter = 0
  NUL = ''
  # FMT = '{id:>3}  {prefix:>12}  {string:>12}  {size:>4}  {children}'
  FMT = '{id:>3}  {prefix:>12}  {size:>4}  {n_child:>7}  {children}'

  def __init__(self, prefix=NUL, parent=None):
    self.prefix= prefix
    self.parent = parent
    self.children = []
    self.id = Trie.counter
    self.offset = None
    self.size = 1
    self.n_child = 0
    Trie.counter += 1
  
  def __lt__(self, other):
    return self.id < other.id 
  
  def __eq__(self, other):
    return self.id == other.id
  
  def to_str(self):
    prefix = self.prefix if self.prefix != Trie.NUL else '/'
    s = Trie.FMT.format(id=self.id, prefix=prefix, size=self.size, n_child=self.n_child,
       children=[child.id for child in self.children])
    L = [s]
    for child in self.children:
      L += child.to_str()
    return L
  
  def __str__(self):
    header = Trie.FMT.format(id='id', prefix='ch', size='size', n_child='n_child', 
    children='children')
    return '\n'.join([header] + self.to_str())
  
  def destruct(self):
    if self.children == []:
      return [self.prefix]
    L = []
    for child in self.children:
      L += [self.prefix + e for e in child.destruct()]
    return L

  @staticmethod
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

  def common_prefix(self, r, i):
    s = self.prefix
    while i < len(s) and i < len(r) and s[i] == r[i]:
      i += 1
    return i

  def replace_with(self, other):
    other.parent = self.parent
    other.size = self.size
    if self.parent:
      self.parent.children[self.offset] = other
      other.offset = self.offset

  @staticmethod
  def construct(ss):
    from itertools import islice
    root = Trie(ss[0])
    for s in islice(ss, 1, None):
      if s == 'ad':
        _____ = 0
      node = root
      i = node.common_prefix(s, 0)
      l = 0
      while True:
        s = s[i:]
        # Split if there is a partial match in the current prefix
        if i < len(node.prefix):
          split_node = Trie(node.prefix[:i])
          node.replace_with(split_node)
          node.prefix = node.prefix[i:]
          new_node = Trie(s, parent=split_node)
          split_node.children = [node, new_node]
          split_node.n_child = 2
          split_node.size += 1
          node.parent = split_node
          node.offset = 0
          new_node.offset = 1
          if node == root:
            root = split_node
          break
        elif node.children == []:
          epsilon = Trie('', parent=node)
          new_node = Trie(s, parent=node)
          node.children = [epsilon, new_node]
          node.n_child = 2
          node.size += 1
          epsilon.offset = 0
          new_node.offset = 1
          break
        # Continue to search downward if current prefix is matched completely
        else:
          node.size += 1
          found = False
          for child in node.children:
            i = child.common_prefix(s, 0)
            if i > 0:
              found = True
              break
          if found:
            l += len(node.prefix)
            node = child
          else:
            new_node = Trie(s, parent=node)
            new_node.offset = len(node.children)
            node.children.append(new_node)
            node.n_child += 1
            break
    return root


def bundling(ss, K):
  t = Trie.construct(ss)
  q = PQueue()
  s = Stack()
  level = 0
  d = 0
  s.push((level, t))
  while not s.empty():
    level, node = s.pop()
    next_level = level + len(node.prefix)
    d = max(d, next_level)
    if len(node.children) > 0:
      q.put((-next_level, node))
    for child in node.children:
      s.push((next_level, child))

  # print("Constructed")
  score = 0
  # Start at the second deepest level
  while not q.empty():
    level, node = q.get()
    d = -level
    p = node.prefix
    # push leftover children up a level
    n_left = node.n_child % K
    n_grouped = node.n_child - n_left
    score += (n_grouped // K) * d
    if node.parent:
      node.parent.n_child += n_left - 1
  return score

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
  t = Trie.construct_fast(ss)
  print("end")
  print(sorted(t.destruct()) == sorted(ss))

def test_trie():
  num_str = 20
  max_strlen = 5
  trials = 10**5
  alpha = [chr(ord('A')+i) for i in range(10)]
  for trial in range(10**5):
    words = []
    if trial % 100 == 0:
      print(trial)
    for _ in range(num_str):
      word = ''.join(choices(alpha, k=random.randint(1,max_strlen)))
      words.append(word)
      words.sort()
    # print(words)
    if words != sorted(Trie.construct_fast(words).destruct()):
      print(words)
      break

if __name__ == '__main__':
  bundling_main()