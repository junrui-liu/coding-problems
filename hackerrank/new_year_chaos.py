#!/usr/bin/env python3

class BSTNode():
  def __init__(self, x):
    self.v = x
    self.l = None
    self.r = None
    self.size = 1

class BST():
  def __init__(self):
    self.root = None
  
  def insert(self, x):
    leaf = BSTNode(x)
    if self.root is None:
      self.root = leaf
    else:
      node = self.root
      while True:
        if x < node.v:
          node.size += 1
          if node.l is not None:
            node = node.l
          else:
            node.l = leaf
            break
        elif x > node.v:
          node.size += 1
          if node.r is not None:
            node = node.r
          else:
            node.r = leaf
            break
        else:
          raise ValueError("Repeated value " + str(x))
  
  def leq(self, hi):
    if self.root is None:
      return 0
    count = 0
    node = self.root
    while node is not None:
      if hi >= node.v:
        if node.l is not None:
          count += node.l.size
        count += 1
        node = node.r
      elif hi < node.v:
        node = node.l
    return count
  
  def lt(self, hi):
    return self.leq(hi-1)

  def __str__(self):
    def to_str(node):
      if node == None:
        return "()"
      else:
        return "({} {} {})".format(str(node.v), to_str(node.l), to_str(node.r))
    return to_str(self.root)

def new_year_chaos(ns):
  import itertools
  bst = BST()
  total_bribes = 0
  for i in range(len(ns)-1,-1,-1):
    print(len(ns)-i)
    n = ns[i]
    bribes = 0
    for j in range(i+1, len(ns)):
      if ns[j] < n:
        bribes += 1
    # bribes = bst.lt(n)
    if bribes > 2:
      return "Too chaotic"
    else:
      # bst.insert(n)
      total_bribes += bribes
  return total_bribes

def new_year_chaos_main():
  t = int(input())
  for ti in range(t):
    _ = int(input())
    ns = [int(c) for c in input().split()]
    print(new_year_chaos(ns))

if __name__ == "__main__":
    new_year_chaos_main()
    # print(new_year_chaos([2,1,5,3,4]))
    # print(new_year_chaos([2,5,1,3,4]))
    # b = BST()
    # b.insert(4)
    # b.insert(3)
    # b.insert(1)
    # b.insert(10)
    # b.insert(2)
    # b.insert(8)
    # b.insert(9)
    # b.insert(7)
    # b.lt(3)
    # b.between(3,10)
    
    
