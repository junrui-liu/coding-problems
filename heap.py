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