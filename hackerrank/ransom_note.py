#!/bin/python3

import math
import os
import random
import re
import sys

def checkMagazine(xs, ys):
  d = dict()
  for x in xs:
    if x in d:
      d[x] += 1
    else:
      d[x] = 1
  for y in ys:
    if y not in d or d[y] <= 0:
      print("No")
      return
    else:
      d[y] -= 1
  print("Yes")
  return

def twoStrings(r,s):
  r_set = set([c for c in r])
  for c in s:
    if c in r_set:
      return "YES"
  return "NO"

def sub_palindromes(s):
  print(s)
  from itertools import combinations
  res = list()
  chars = dict()
  for i,c in enumerate(s):
    if c in chars:
      chars[c].add(i)
    else:
      chars[c] = {i}
  
  for c in chars:
    for i,j in combinations(chars[c], 2):
      i,j = min(i,j), max(i,j)
      # add all 1-anagrams
      res.append((i,j,1))
      # build k-anagrams for k >= 2
      for d in range(1,j-i):
        if s[i+d] == s[j-d]:
          res.append((i,j,d+1))
        else:
          break
  print(len(res))
  for i,j,l in res:
    print(i, j, l, s[i:i+l], s[j-l+1:j+1])
  return res

def anagrams(s):
  def sort_str(s):
    return "".join(sorted([c for c in s]))

  d = dict()
  subs = set()
  for i in range(len(s)):
    for j in range(i,len(s)):
      sub = sort_str(s[i:j+1])
      if sub in d:
        d[sub].append(i)
        subs.add(sub)
      else:
        d[sub] = [i]
  total = 0
  for sub in subs:
    n = len(d[sub])
    total += n * (n-1) // 2
  return total

def count_triples(ns, r):
  from collections import defaultdict
  if r > 1:
    inverse = defaultdict(lambda: 0)
    pairs = defaultdict(lambda: 0)
    count = 0
    for a3 in ns:
      inverse[a3] += 1
      a2 = a3 // r if a3 % r == 0 else None
      a1 = a2 // r if a2 is not None and a2 % r == 0 else None
      if not (a1 is None and a2 is None) and (a1,a2) in pairs:
        count += pairs[(a1,a2)]
      if a2 is not None and a2 in inverse:
        pairs[(a2,a3)] += inverse[a2]
    return count
  else:
    def fact(n):
      p = 1
      while n > 0:
        p = n * p
        n -= 1
      return p
    def choose(n, r):
      p = 1
      for i in range(r):
        p *= (n-i)
      return p // fact(r)
    inverse = defaultdict(lambda: 0)
    for n in ns:
      inverse[n] += 1
    return sum(choose(inverse[n], 3)for n in inverse)

def frequent_queries_naive(qs):
  from collections import defaultdict
  ans = []
  xs = []
  for q, x in qs:
    if q == 1:
      xs.append(x)
    elif q == 2:
      for i in range(len(xs)):
        if xs[i] == x:
          xs = xs[:i] + xs[i+1:]
          break
    elif q == 3:
      count = defaultdict(lambda: 0)
      res = 0
      for y in xs:
        count[y] += 1
        if count[y] == x:
          res = 1
          break
      ans.append(res)
  return ans

def frequent_queries(qs):
  from collections import defaultdict
  count = defaultdict(lambda: 0)
  freq = defaultdict(lambda: 0)
  ans = []
  for q,x in qs:
    if q == 1:
      freq[count[x]] -= 1
      count[x] += 1
      freq[count[x]] += 1
    elif q == 2:
      if count[x] > 0:
        freq[count[x]] -= 1
        count[x] -= 1
        freq[count[x]] += 1
    elif q == 3:
      if freq[x] > 0:
        ans.append(1)
      else:
        ans.append(0)
    else:
      raise ValueError("Invalid query")
  return ans


if __name__ == '__main__':
    fptr = sys.stdout

    q = int(input().strip())

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    ans = frequent_queries(queries)

    fptr.write('\n'.join(map(str, ans)))
    fptr.write('\n')

    fptr.close()