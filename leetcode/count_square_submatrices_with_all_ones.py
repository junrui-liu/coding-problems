def solve_slow(A):
  from collections import defaultdict
  m, n = len(A), len(A[0])
  total = 0
  B = None
  S = None
  for s in range(m+n-1):
    B0, B = B, defaultdict(lambda: 0)
    S0, S = S, defaultdict(set)
    # stores # of squares that end at (i,j) with length k
    if s < n:
      i,j = 0,s
    else:
      i,j = s-n+1, n-1
    while i < m and j >= 0:
      if A[i][j] == 1:
        B[(i,j,1)] = 1 # square of length 1
        S[(i,j)].add(1)
        total += 1
        S_left = S0[(i,j-1)] if j>0 else set()
        S_above = S0[(i-1,j)] if i>0 else set()
        for k0 in S_left & S_above:
          k = k0+1
          if A[i-k+1][j-k+1] == 1:
            B[(i,j,k)] = min(B0[(i,j-1,k-1)], B0[i-1,j,k-1])
            if B[(i,j,k)] > 0:
              S[(i,j)].add(k)
              total += B[(i,j,k)]
      i, j = i+1, j-1
  return total

def solve(A):
  from collections import defaultdict
  m, n = len(A), len(A[0])
  total = 0
  C = None # cache
  # iterate through pts on the diagonals by distance to (0,0)
  for s in range(m+n-1):
    # stores maximum length of square whose southeast corner touches (i,j)
    C, C0 = dict(), C
    # generate the north-east endpoint using the diagonal number
    if s < n:
      i,j = 0,s
    else:
      i,j = s-n+1, n-1
    # walk southwest along the diagonal
    while i < m and j >= 0:
      if A[i][j] == 1: # (i,j) will introduces new squares
        # check if there are squares ending left and above
        if C0 is not None and (i-1,j) in C0 and (i,j-1) in C0: 
          maxlen_left = C0[( i, j-1 )]
          maxlen_above = C0[( i-1, j )]
          if maxlen_left == maxlen_above:
            l = maxlen_left
            # the upper-left tip is also 1, making a larger square
            if A[i-l][j-l] == 1:
              l += 1
          # the smaller length + 1 bounds the current length
          else:
            l = min(maxlen_left, maxlen_above) + 1
        else:
          l = 1 # no neighbors, so (i,j) itself is the largest square
        C[(i,j)] = l
        total += l # one new square for each length in [1, 2, ..., l]
      i, j = i+1, j-1
  return total