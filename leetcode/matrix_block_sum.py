def solve_block(A, K):
  # Slow
  m, n = len(A), len(A[0])
  def force_inside(ra, rb, ca, cb):
    return max(0, ra), min(m, rb), max(0, ca), min(n, cb)

  def rect(i, j):
    return force_inside(i-K, i+K+1, j-K, j+K+1)

  def sum_rect(ra, rb, ca, cb):
    ra, rb, ca, cb = force_inside(ra, rb, ca, cb)
    s = 0
    for p in range(ra,rb):
      for q in range(ca, cb):
        s += A[p][q]
    return s

  S = [[0 for j in range(n)] for i in range(m)]
  for i in range(m):
    for j in range(n):
      ra, rb, ca, cb = rect(i,j)
      if i == 0 and j == 0:
        S[i][j] = sum_rect(ra, rb, ca, cb)
      else:
        if j == 0:
          i0, j0 = i-1, 0
        else:
          i0, j0 = i, j-1
        ra0, rb0, ca0, cb0 = rect(i0,j0)
        S[i][j] = S[i0][j0]
        S[i][j] -= sum_rect(ra0, ra, ca, cb)
        S[i][j] -= sum_rect(ra, rb, ca0, ca)
        S[i][j] += sum_rect(rb0, rb, ca, cb)
        S[i][j] += sum_rect(ra, rb, cb0, cb)
  return S

def solve_prefix_sum(A,K):
  # Fast
  m, n = len(A), len(A[0])
  B = [[A[i][j] for j in range(n)] for i in range(m)]
  S = [[None for j in range(n)] for i in range(m)]
  def compute(S, B, i, j):
    ra, rb, ca, cb = max(0,i-K), min(m-1,i+K), max(0,j-K), min(n-1,j+K)
    S[i][j] = B[rb][cb]
    if ra > 0:
      S[i][j] -= B[ra-1][cb]
    if ca > 0:
      S[i][j] -= B[rb][ca-1]
    if ra > 0 and ca > 0:
      S[i][j] += B[ra-1][ca-1]

  for i in range(m):
    for j in range(n):
      if i > 0:
        B[i][j] += B[i-1][j]
      if j > 0:
        B[i][j] += B[i][j-1]
      if i > 0 and j > 0:
        B[i][j] -= B[i-1][j-1]
      r,c = i-K, j-K
      if r >=0 and c >= 0:
        compute(S, B, r, c)

  for i in range(max(0,m-K),m):
    for j in range(0,n):
      compute(S,B,i,j)
  for i in range(0,m-K):
    for j in range(max(0,n-K),n):
      compute(S,B,i,j)      
  return S

s = solve_prefix_sum([[17,81],[47,51],[32,20],[48,13],[73,27],[63,57],[30,47],[81,62],[66,33],[78,5],[75,93],[74,62],[41,54],[86,96],[24,5],[26,15],[88,73],[52,77],[93,87],[70,46],[49,71],[87,30],[5,79],[59,43],[15,21],[36,98],[42,37],[48,37],[39,36],[56,12],[56,96],[21,13],[69,18],[29,43],[8,11],[25,92],[50,32],[93,82],[72,77],[51,74],[12,95],[14,49],[13,70],[16,78],[9,44],[96,95],[64,86],[74,19],[55,76],[83,32]], 38)
      
        
      
