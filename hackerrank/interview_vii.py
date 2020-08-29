def getMatches(events):
  from collections import defaultdict
  followers = defaultdict(set)
  res = list()
  for a,b in events:
    followers[b].add(a)
    if b in followers[a]:
      res.append( (b,a) )
  return res

def wifiZones(zones):
  without = 0
  i = 0
  a1,b1 = zones[i]
  while i < len(zones):
    for j in range(i+1,len(zones)):
      a2,b2 = zones[j]
      if b2 >= b1:
        i = j
        if b1 < a2:
          without += a1-b1
        break





def findPalindrome(s, num_q, pos_l, ch_l):
  s = [ch for ch in s]
  # two-letter palindrome
  p2 = set()
  for i in range(len(s)-1):
    if s[i] == s[i+1]:
      p2.add( i )
  # three-letter palindrom
  p3 = set()
  for i in range(1,len(s)-1):
    if s[i-1] == s[i+1]:
      p3.add( i )
  res = list()
  for q in range(len(pos_l)):
    i, ch = pos_l[q], ch_l[q]
    s[i] = ch
    # check for two-letter palindromes (i,i+1) and (i-1,i)
    if i < len(s)-1:
      if s[i] == s[i+1]:
        p2.add( i )
      elif i in p2:
        p2.remove( i )
    if i > 0:
      if s[i-1] == s[i]:
        p2.add( i-1 )
      elif i in p2:
        p2.remove( i-1 )
    # check for three-letter palindromes centered
    # at i-1 (i-2,i-1,i) and i+1 (i,i+1,i+2) (no need to check i)
    if i-2 >= 0:
      if s[i-2] == s[i]:
        p3.add( i-1 )
      elif i-1 in p3:
        p3.remove( i-1 )
    if i+2 < len(s):
      if s[i] == s[i+2]:
        p3.add( i+1 )
      elif i+1 in p3:
        p3.remove( i+1 )
    if len(p2) > 0 or len(p3) > 0:
      res.append("Yes")
    else:
      res.append("No")
  return res
    
      
