#!/usr/bin/env python3
def read(conv):
  while True:
    s = input().strip()
    if s != "":
      return [conv(s) for s in s.split()]

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)
      
def foregone(n):
  s = str(n)
  a = int("".join(["2" if c == "4" else c for c in s]))
  b = int("".join(["2" if c == "4" else "0" for c in s]))
  return a,b

def foregone_main():
  num_tests = int(input())
  for i in range(num_tests):
    n = int(input())
    a,b = foregone(n)
    print("Case #{}: {} {}".format(i+1, a, b))

def maze(s):
  return "".join(["S" if c == "E" else "E" for c in s])

def maze_main():
  num_tests = int(input())
  for i in range(num_tests):
    n = int(input())
    moves = input().strip()
    moves_ = maze(moves)
    print("Case #{}: {}".format(i+1, moves_))

def gcd(a,b):
  def _gcd(a,b):
    while True:
      if a == b:
        return a
      if a == 0:
        return b
      elif b == 0:
        return a
      else:
        c = b-a
        if a <= c:
          a,b = a,c
        else:
          a,b = c,a
  if a <= b:
    return _gcd(a,b)
  else:
    return _gcd(b,a)

def crypto(ns):
  def unzip(ns, key):
    ps = []
    ps_set = {key}
    p = key
    for n in ns:
      q = n // p
      ps.append(q)
      ps_set.add(q)
      p = q
    return ps, ps_set
  
  for i in range(1, len(ns)):
    if ns[i] != ns[i-1]:
      key = gcd(ns[i], ns[i-1])
      break
  ps1, ps_set1 = unzip(ns[i-1::-1], key)
  ps2, ps_set2 = unzip(ns[i:], key)
  ps = ps1[::-1] + [key] + ps2
  ps_set = ps_set1 | ps_set2
  d = dict()
  for i,p in enumerate(sorted(list(ps_set))):
    d[p] = chr(ord('A') + i)
  return "".join([d[p] for p in ps])

def crypto_main():
  num_tests = int(input())
  for i in range(num_tests):
    N_L = input().split()
    N = N_L[0]
    L = N_L[1]
    ns = [int(s) for s in input().strip().split()]
    print("Case #{}: {}".format(i+1, crypto(ns)))

# def dat_update(bsize, msg, rpl, old_info):
#   print(bsize, msg, rpl, old_info)
#   old_bsize = bsize * 2
#   old = 0
#   new = 0
#   expect = 0
#   new_info = []
#   remaining = bsize
  
#   def flip(n): return 1-n

#   def skip_broken_block():
#     nonlocal new_info, new, old, remaining, expect
#     while old < len(old_info) and \
#       (expect == 1 and remaining == old_info[old] or \
#        expect == 0 and remaining + bsize == old_info[old]):
#       new_info.append(remaining)
#       expect = flip(expect)
#       new += 1
#       if remaining + bsize == old_info[old]:
#         expect = flip(expect)
#         new_info.append(bsize)
#         new += 1
#       remaining = bsize
#       old += 1
  
#   for i, d in enumerate(rpl):
#     skip_broken_block()
#     if bsize == 1:
#       j = 1
#     # breakpoint()
#     if d != expect:
#       new_info.append(remaining)
#       remaining = bsize - 1
#       expect = flip(expect)
#       new += 1
#       if expect == 0:
#         old += 1
#     elif d == expect:
#       remaining -= 1
#   new_info.append(remaining)
#   new += 1
#   while (new < len(msg) // bsize):
#     new_info.append(bsize)
#     new += 1
#   return new_info


def group(xs, n):
  res = []
  while len(xs) > n:
    res.append(xs[:n])
    xs = xs[n:]
  if len(xs) > 0:
    res.append(xs)
  return res


def update(msg, rpl, info, bsize):
  if bsize == 2:
    j = 1
  
  msg, rpl, info, n_good, acc = group(msg, bsize), rpl, info, 0, []
  while True:
    if msg == []:
      break
    elif len(info) > 0 and n_good + info[0] >= bsize: # exhausted non-broken slots in the head block
      acc.extend( [None] * len(msg[0]) )
      msg, rpl, info, n_good, acc = msg[1:], rpl, info[1:], 0, acc
    elif msg[0] == []: # nothing else to match in the head block
      msg, rpl, info, n_good, acc = msg[1:], rpl, info[1:], n_good, acc
    elif len(rpl) == 0: # base case
      acc.extend([None] * len([1 for block in msg for _ in block]))
      break
    else: # try to match
      hd, tl = msg[0], msg[1:]
      new_msg = [hd[1:]] + tl
      if rpl[0] == hd[0]:
        msg, rpl, info, n_good, acc =new_msg, rpl[1:], info, n_good+1, acc + [rpl[0]]
      else: # found a broken slot
        msg, rpl, info, n_good, acc =new_msg, rpl, info, n_good, acc + [None]
  match_res = acc
  count_broken = lambda block: sum((1 for x in block if x is None))
  return [count_broken(g) for g in group(match_res, bsize // 2)]


def dat_quiz():
  import random, pprint
  random.seed(1)
  def quiz(n,b):
    import random, math
    size_log = math.ceil(math.log2(n))
    size = 2 ** size_log
    ns = [False for _ in range(size)]
    for broken in random.sample(list(range(size)),b):
      ns[broken] = True
    info = []
    for i in range(size_log-1, -1, -1): # 2**4 = 16 down to 2**0 = 1
      block_size = 2**i
      msg = []
      for j in range(len(ns) // block_size):
        if j % 2 == 0:
          msg += [0] * block_size
        else:
          msg += [1] * block_size
      rpl = [m for (b,m) in zip(ns, msg) if not b]
      info = update(msg, rpl, info, block_size * 2)
      # print("Block size: %d" % (2**i))
      # print("Send", ''.join([str(i) for i in msg]))
      # print("Got", ''.join([str(i) for i in rpl]))
      # print(info)
      
    if [1 if b else 0 for b in ns] != info:
      print(n,b)
      # print(info)
    # print("Answer:")
    # _ = input()
    # for n in range(len(ns)):
    #   print("%3d" % n, end="")
    # print()
    # for b in ns:
    #   x = "X" if b else ""
    #   print("%3s" % x, end="")
    # print()

  # while True:
  #   n_b = read(int)
  #   n = n_b[0]
  #   b = n_b[1]
  for N in range(2,1024+1):
    print(N)
    for B in range(1, min(15, N-1)+1):
      # print(N, B)
      for t in range(100):
        quiz(N, B)

def dat_main():
  import math
  T = int(input())
  for t in range(T):
    n_b_f = read(int)
    n = n_b_f[0]
    b = n_b_f[1]
    f = n_b_f[2]
    size_log = math.ceil(math.log2(n))
    size = 2 ** size_log
    info = []
    for i in range(size_log-1, -1, -1): # 2**4 = 16 down to 2**0 = 1
      block_size = 2**i
      msg = []
      for j in range(size // block_size):
        if j % 2 == 0:
          msg += [0] * block_size
        else:
          msg += [1] * block_size
      import sys
      # eprint("Send: ", msg[:n])
      print("".join((str(_i) for _i in msg[:n])))
      rpl = [int(c) for c in input()] + msg[n:]
      info = update(msg, rpl, info, block_size * 2)
    # eprint(info)
    print(" ".join([str(_i) for _i,b in enumerate(info[:n]) if b == 1]))
    success = input() == "1"
    # eprint("Success", success)

if __name__ == "__main__":
  dat_quiz()