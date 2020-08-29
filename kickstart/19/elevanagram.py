def covering(i):
  success = False
  ct = 10
  while not success:
    covered = [False for _ in range(11)]
    n_to_cover = 10
    for n_odd in range(ct):
      n_even = ct - n_odd
      r = (n_odd - n_even) * i % 11
      if not covered[r]:
        covered[r] = True
        n_to_cover -= 1
      if n_to_cover == 0:
        return ct
    ct += 1

covering(4)