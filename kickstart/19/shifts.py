# Input template
try:
    input = raw_input
except NameError:
    pass

def read_ints():
  return [int(i) for i in raw_input().split()]

def read_int_arr():
  return list(map(int, raw_input().split()))

def explode(s):
  return [ch for ch in s]

def read_input():
  num_cases = int(input())
  for t in range(1, num_cases+1):
    N, H = read_ints()
    xs = read_int_arr()
    ys = read_int_arr()
    res = solve(N, H, xs, ys)
    print("Case #{}: {}".format(t, res))

# Solution begins here

  

def solve(N, H, xs, ys):
  # print(xs, ys)
  xs_ys = list(zip(xs,ys))
  xs_ys.sort(key=lambda p: max(*p), reverse=True)
  fst, snd = lambda p: p[0], lambda p: p[1]
  xs, ys = list(map(fst, xs_ys)), list(map(snd, xs_ys))
  # print(xs, ys)
  # postfix sum for xs and ys
  px = [0 for _ in range(N+1)]
  py = [0 for _ in range(N+1)]
  for i in range(N-1, -1, -1):
    px[i] = xs[i] + px[i+1]
    py[i] = ys[i] + py[i+1]

  def dp(i, hx, hy):
    if i == N and hx >= H and hy >= H:
      return 1
    elif hx + px[i] < H or hy + py[i] < H:
      return 0
    elif hx >= H and hy >= H:
      return int( 3 ** (N-i) )
    elif hx >= H: # x doesn't have to work today
      # if x works, then y can work or not; else, y must work
      # so y works in two cases and doesn't work in one case
      return dp(i+1, hx, hy) + \
             dp(i+1, hx, hy + ys[i]) * 2
    elif hy >= H: # y doesn't have to work today
      return dp(i+1, hx, hy) + \
             dp(i+1, hx + xs[i], hy) * 2
    else:
      return dp(i+1, hx + xs[i], hy) +\
             dp(i+1, hx, hy + ys[i]) +\
             dp(i+1, hx + xs[i], hy + ys[i])
  return dp(0, 0, 0)

if __name__ == "__main__":
  read_input()
  # solve(2, 3, [1, 2], [3, 3])
  # solve(0, 0, [1 for _ in range(20)], [1 for _ in range(20)])