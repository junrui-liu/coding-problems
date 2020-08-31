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