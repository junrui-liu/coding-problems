def solution(A):
    # write your code in Python 3.6
    if len(A) <= 4:
        return 0
    A = sorted(A)
    l = len(A)
    min_amp = None
    for i in range(0,3+1): # i = 0,1,2,3
        j = l - (3 - i)
        amp = A[j-1]-A[i]
        if min_amp is None or amp < min_amp:
            min_amp = amp
    return min_amp
        
def solution(S):
  from collections import Counter
  c1 = Counter()
  c2 = Counter(S)
  count = 0
  for i in range(len(S)):
    ch = S[i]
    c1[ch] += 1
    c2[ch] -= 1
    if c2[ch] <= 0:
      del c2[ch]
    if len(c1) == len(c2):
      count += 1
  return count

if __name__ == "__main__":
  from random import choices
  alphabet = range(26)
  print(solution('a' * 10))

  