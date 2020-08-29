import sys
import random
if __name__ == "__main__":
  L, filename = sys.argv[1:]
  L = int(float(L))
  VAL_L = 100
  gen_val = lambda: random.randrange(VAL_L)+1
  gen_ind = lambda: random.randrange(L)+1
  xs = [gen_val() for _ in range(L)]
  qs = []
  for _ in range(L):
    if random.random() < 0.5:
      op = "U"
      i, v = gen_ind(), gen_val()
      line = "{} {} {}".format(op, i, v)
    else:
      op = "Q"
      i, j = gen_ind(), gen_ind()
      l, r = min(i,j), max(i,j)
      line = "{} {} {}".format(op, l, r)
    qs.append(line)
  with open("candies.test2", "w") as outfile:
    outfile.write("1\n10000 10000\n")
    outfile.write(" ".join(map(str, xs)))
    outfile.write("\n")
    for q in qs:
      outfile.write(q + '\n')