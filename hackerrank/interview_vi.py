def array_sum_operation(n, ops):
  xs = [i+1 for i in range(n)]
  elems = set()
  total = (1+n)*n//2
  res = list()
  for op in ops:
    if op in elems:
      xs[0], xs[-1] = xs[-1], xs[0]
      res.append(total)
    else:
      total = total - xs[-1] + op
      res.append(total)
      elems.remove(xs[-1])
      elems.add(op)
      xs[-1] = op
  return res

def construct_tree(n,x):
  n -= 1 # don't count the root
  if n == 0 and x == 0:
    return []
  # An (n,x) tree is possible if and only if n <= x (all nodes have depth 1)
  # and n*(n+1)//2 >= x (linear path with total depths = arithmetic sum 1...n)
  if n > x or n*(n+1)//2 < x:
    return [(-1,-1)]
  # Otherwise, every tree of (n,x) is achievable
  # To see this, start with the lowest-score tree (n,n), where all nodes have depth 1.
  # Promote a node from depth 1 to 2 increases the score by 1.
  # Do this for n-1 nodes, and we filled level 2.
  # Repeatedly promote nodes and fill each level until we reach a score of x.
  
  # A [filled tree] has a linear path with k-1 nodes, and a flat bush with n-(k-1) nodes at depth k
  filled_score = lambda k: k*(k-1)//2 + k*(n-k+1)

  def direction(k):
    if x > filled_score(k):
      return 1
    elif x <= filled_score(k-1):
      return -1
    else:
      return 0

  lo = 1
  hi = n
  while lo < hi:
    mid = (lo + hi) // 2
    d = direction(mid)
    if d > 0:
      lo = mid + 1
    elif d < 0:
      hi = mid - 1
    else:
      lo, hi = mid, mid
  assert(lo == hi)
  k = lo # current level
  prev_filled_score = filled_score(k-1) if k > 0 else 0
  res = list()
  count = 1
  n_linear = max(0, k-2) # number of linear nodes of depths 0, 1, ..., k-1
  n_current = max(0, x - filled_score(k-1)) # partially fill level k
  n_prev = max(0, n - n_linear - n_current) # the remaining nodes partially fill level k-1
  # Output the edges
  count = 1
  for _ in range(n_linear):
    res.append(( count-1, count ))
    count += 1
  for _ in range(n_prev):
    res.append(( k-2, count ))
    count += 1
  for i in range(n_current):
    res.append(( k-1, count ))
    count += 1
  return list(map(lambda p: (p[0]+1,p[1]+1), res))

def solving_for_queries_with_cups(n, balls, swaps, queries):
  # print(n, balls, swaps, queries)
  balls = set(map(lambda i:i-1, balls))
  for i,j in swaps:
    i, j = i-1, j-1
    # if cup x contains a ball and cup y doesn't,
    # then remove x from the set and add y to it
    if i in balls and j not in balls:
      balls.remove(i)
      balls.add(j)
    elif j in balls and i not in balls:
      balls.remove(j)
      balls.add(i)

  def binary_search(L, R, check):
    lo, hi = L, R
    # Invariant: lo < min pos that passes check, hi > max pos that passes check
    while lo +1 < hi:
      mid = (lo + hi) // 2
      # at least one between lo and hi, so L <= lo < mid < hi <= R
      c = check(mid)
      if c > 0:
        lo = mid
      elif c < 0:
        hi = mid
      else:
        return mid-1, mid+1 # lo +2 == mid +1 == hi, where mid passes check
    # loop breaks only when lo +1 == hi
    return lo, hi

  balls = list(balls)
  balls.sort()
  B = len(balls)
  res = list()
  for l,r in queries:
    l, r = l-1, r-1
    i_lo, i_hi = binary_search(-1, B, lambda i: l-balls[i])
    # i_lo is the maximum index that fails the check, so i_lo+1 passes if it's valid
    i = i_lo +1
    j_lo, j_hi = binary_search(-1, B, lambda i: r-balls[i])
    # j_hi is the minimum index that fails the check, so j_hi-1 passes if it's valid
    j = j_hi -1
    if i >= B or j < 0: # requested interval contains no ball
      res.append(0)
    else:
      i, j = max(i, 0), min(B-1, j)
      res.append(j-i+1)
  return res

class UF:
  def __init__(self, n):
    self.n = n # total number of elements
    self.p = list(range(n)) # parent
    self.s = [1 for _ in range(n)] # subtree size
  def is_root(self, i):
    return self.p[i] == i
  def find(self, i):
    parent = self.p[i]
    if parent == i:
      return i
    r = self.find(parent)
    self.p[i] = r
    return r
  def union(self, i, j):
    ri, rj = self.find(i), self.find(j)
    if ri == rj: return
    if self.s[ri] < self.s[rj]:
      smaller, larger = ri, rj
    else:
      smaller, larger = rj, ri
    self.p[smaller] = larger
    self.s[larger] += self.s[smaller]
  def connected(self, i, j):
    return self.find(i) == self.find(j)
  def num_components(self):
    return sum( (1 for i in range(self.n) if self.is_root(i)) )
  def components(self):
    return [ i for i in range(self.n) if self.is_root(i) ]
  def depth(self, i):
    count = 0
    while self.p[i] != i:
      i = self.p[i]
      count += 1
    return count
  def all_depth(self):
    return [self.depth(i) for i in range(self.n)]
  def random_test(self):
    N = int(1e6)
    import random; randi = lambda: random.randint(0,N-1)
    import itertools; argmax = lambda l: max(zip(itertools.count(), l),key=lambda p:p[1])[0]
    u = UF(N)
    for _ in range(int(1e5)):
      i,j = randi(), randi()
      u.union(i,j)
    return u

def rerouting(connections):
  # First attempt using union-find
  # from collections import defaultdict
  # # Auxillary structures
  # n = len(connections)
  # uf = UF(n)
  # for u,v in enumerate(connections):
  #   v -= 1
  #   uf.union(u,v)
  # families = 0
  # singletons = 0
  # for i in range(n):
  #   if uf.is_root(i):
  #     if uf.s[i] > 1:
  #       families += 1
  #     else:
  #       singletons += 1
  # if singletons > 0:
  #   return families + (singletons - 1)
  # else:
  #   return families

  # Second attempt using DFS
  from collections import defaultdict
  def next_hop(i):
    return connections[i]-1
  cycles_multi = 0
  cycles_single = 0
  n = len(connections)
  visited = [False for _ in range(n)]
  ids = [-1 for _ in range(n)]
  for i in range(n):
    j = i
    while not visited[j]:
      visited[j] = True
      ids[j] = i # j is in i's component
      j = next_hop(j)
    if ids[j] == i: # new cycle on the current dfs path
      if next_hop(j) == j:
        cycles_single += 1
      else:
        cycles_multi += 1
    # else we found a visited route (cycle)    
  if cycles_single > 0:
    return cycles_multi + cycles_single -1
  else:
    return cycles_multi





l04 = [218, 654, 803, 736, 749, 448, 104, 900, 1052, 881, 944, 880, 1353, 1083, 153, 1258, 454, 1076, 949, 104, 788, 1094, 60, 161, 943, 415, 870, 863, 145, 860, 1264, 474, 15, 1200, 670, 1091, 1277, 1123, 892, 909, 675, 1208, 210, 926, 1098, 1059, 1329, 1140, 381, 749, 1372, 1228, 283, 124, 1232, 6, 1098, 810, 563, 968, 1303, 1257, 249, 1295, 267, 829, 928, 788, 998, 1312, 517, 1144, 773, 902, 1323, 814, 480, 22, 538, 392, 591, 731, 1330, 258, 995, 838, 471, 506, 234, 919, 684, 998, 1187, 559, 210, 717, 150, 1318, 1060, 97, 1312, 858, 818, 1306, 155, 525, 1311, 1161, 1356, 368, 215, 276, 969, 414, 1007, 1315, 28, 1186, 774, 1032, 1339, 409, 1187, 1184, 624, 972, 667, 902, 346, 518, 1368, 642, 480, 1081, 472, 372, 853, 439, 660, 1270, 1219, 735, 710, 1037, 851, 1107, 337, 1004, 387, 794, 1313, 589, 1060, 280, 518, 641, 434, 750, 295, 914, 344, 629, 927, 201, 365, 828, 579, 44, 252, 297, 720, 781, 269, 1185, 99, 90, 35, 928, 471, 165, 1126, 821, 500, 985, 152, 1235, 1217, 1321, 1038, 797, 613, 899, 337, 523, 723, 507, 1248, 1098, 206, 317, 931, 285, 911, 265, 1262, 1074, 253, 574, 1115, 364, 1203, 1091, 651, 1147, 611, 1197, 1192, 184, 1316, 477, 560, 1081, 24, 942, 1330, 324, 1156, 730, 546, 472, 1207, 1280, 206, 660, 291, 596, 266, 847, 1221, 916, 992, 1283, 1012, 803, 643, 452, 627, 325, 747, 683, 941, 548, 1046, 1095, 848, 288, 737, 1187, 446, 1299, 116, 430, 78, 594, 1206, 278, 565, 1120, 1192, 103, 865, 904, 58, 679, 803, 121, 533, 454, 35, 708, 583, 265, 951, 727, 306, 883, 75, 1261, 1150, 385, 618, 630, 297, 293, 919, 1367, 903, 213, 426, 839, 517, 746, 153, 764, 1106, 45, 1016, 311, 829, 1104, 77, 369, 290, 181, 1100, 904, 572, 721, 1069, 390, 628, 968, 1274, 1303, 291, 1126, 246, 339, 603, 421, 103, 795, 904, 914, 1291, 1055, 156, 663, 1022, 1308, 1062, 1243, 437, 115, 1241, 705, 324, 926, 1080, 1228, 294, 61, 464, 1076, 1242, 231, 1300, 1290, 346, 613, 1013, 1352, 845, 39, 9, 1104, 660, 395, 335, 595, 1331, 489, 323, 1022, 845, 255, 995, 120, 1228, 1298, 361, 423, 1249, 73, 909, 388, 155, 1093, 390, 1039, 601, 291, 1266, 531, 630, 1241, 1033, 1007, 386, 1185, 1211, 626, 684, 120, 1302, 408, 69, 66, 1231, 1082, 568, 836, 519, 1061, 807, 269, 573, 885, 818, 100, 115, 350, 581, 1211, 323, 1239, 467, 1370, 1268, 1091, 1305, 722, 1348, 4, 539, 1118, 391, 267, 717, 1046, 445, 560, 46, 781, 1161, 111, 1139, 548, 621, 198, 87, 873, 1172, 428, 995, 1190, 735, 182, 25, 96, 150, 1290, 952, 985, 238, 471, 185, 278, 775, 1238, 361, 505, 648, 1268, 572, 678, 595, 137, 785, 167, 581, 10, 693, 627, 919, 99, 194, 840, 454, 958, 66, 135, 273, 521, 1238, 1042, 824, 840, 1091, 119, 634, 637, 1224, 395, 749, 1260, 621, 482, 938, 996, 51, 292, 1221, 561, 1185, 1177, 759, 526, 944, 612, 830, 1280, 762, 540, 133, 240, 325, 343, 788, 90, 1193, 818, 983, 1079, 328, 89, 17, 1188, 80, 260, 822, 1016, 686, 812, 1341, 751, 726, 727, 1248, 487, 598, 83, 959, 155, 136, 561, 225, 321, 491, 1186, 409, 864, 160, 99, 152, 1310, 921, 304, 649, 268, 573, 1104, 1341, 383, 393, 251, 782, 924, 985, 379, 725, 195, 248, 975, 1070, 183, 1275, 343, 708, 535, 1276, 496, 1368, 1214, 906, 1194, 66, 279, 86, 950, 1324, 1219, 633, 612, 33, 1252, 540, 1037, 1139, 531, 1265, 619, 1040, 58, 467, 284, 1323, 408, 991, 425, 84, 1291, 568, 746, 183, 350, 374, 1112, 367, 514, 262, 1052, 608, 971, 984, 1368, 812, 24, 169, 676, 41, 1108, 1178, 1109, 454, 1089, 1256, 714, 1263, 1016, 375, 452, 628, 708, 362, 1192, 1046, 24, 206, 816, 807, 258, 281, 489, 1226, 155, 1019, 643, 1098, 200, 517, 1222, 279, 1144, 1261, 141, 1352, 975, 641, 187, 2, 150, 133, 905, 762, 372, 8, 994, 890, 321, 516, 1067, 972, 489, 1115, 1289, 675, 629, 918, 975, 1004, 1073, 796, 305, 819, 377, 54, 444, 38, 116, 1364, 303, 201, 665, 1364, 1138, 1255, 151, 524, 1130, 71, 478, 1128, 149, 700, 1375, 804, 703, 408, 1010, 687, 1320, 247, 1240, 913, 1254, 485, 1222, 747, 1173, 71, 123, 1091, 872, 1048, 635, 1243, 1003, 550, 984, 1152, 999, 1288, 1178, 817, 1359, 901, 534, 1223, 368, 107, 179, 10, 778, 938, 1096, 547, 1361, 426, 1247, 399, 507, 1086, 1256, 354, 1027, 700, 164, 1170, 568, 80, 360, 824, 425, 416, 1085, 91, 711, 1179, 1286, 664, 413, 532, 143, 370, 1158, 993, 395, 466, 506, 559, 694, 1077, 1156, 172, 342, 1110, 431, 1204, 962, 684, 1103, 1311, 1331, 83, 484, 1374, 496, 1343, 137, 703, 850, 1101, 858, 685, 1318, 1317, 263, 49, 963, 614, 69, 1090, 112, 412, 597, 266, 1316, 631, 590, 8, 905, 868, 113, 985, 986, 1059, 284, 297, 918, 775, 428, 650, 1130, 343, 200, 439, 658, 661, 1116, 583, 416, 192, 1168, 636, 1000, 359, 337, 1357, 1212, 770, 677, 264, 1040, 786, 136, 1148, 1329, 740, 131, 798, 686, 476, 137, 271, 529, 1126, 1001, 1015, 646, 416, 575, 124, 884, 1368, 419, 1049, 523, 246, 1096, 696, 432, 625, 1364, 858, 239, 219, 895, 983, 1097, 1106, 189, 611, 561, 1048, 932, 626, 484, 40, 684, 549, 18, 1275, 558, 290, 645, 835, 757, 544, 693, 75, 1131, 1143, 694, 1356, 1348, 1304, 455, 1364, 956, 952, 953, 55, 385, 664, 768, 1018, 668, 1116, 46, 538, 167, 1344, 34, 249, 1157, 1158, 166, 484, 1165, 205, 34, 1213, 667, 233, 1359, 509, 250, 811, 84, 160, 1017, 285, 1133, 163, 561, 498, 1253, 445, 490, 972, 722, 979, 953, 992, 1156, 1038, 1218, 388, 1367, 303, 13, 1017, 595, 410, 822, 1235, 600, 98, 336, 19, 1027, 862, 474, 69, 155, 1303, 912, 288, 1181, 625, 442, 1222, 97, 1096, 1121, 265, 307, 444, 718, 1071, 1358, 583, 179, 16, 518, 303, 681, 1079, 911, 678, 851, 656, 380, 1012, 936, 831, 242, 122, 1070, 1277, 294, 1238, 78, 704, 640, 946, 718, 990, 418, 1124, 249, 137, 727, 1115, 1251, 1374, 461, 930, 416, 1255, 52, 406, 806, 1128, 1247, 604, 650, 968, 142, 288, 884, 1246, 1137, 974, 333, 1377, 765, 529, 871, 1155, 603, 230, 851, 1232, 1028, 812, 936, 251, 816, 358, 1020, 1281, 951, 977, 999, 428, 581, 1354, 1119, 1059, 105, 1109, 398, 1352, 482, 365, 12, 1151, 1029, 324, 1064, 77, 30, 394, 770, 2, 514, 82, 1183, 958, 387, 889, 992, 593, 716, 1257, 1044, 166, 510, 713, 733, 327, 1127, 434, 505, 1216, 1372, 427, 384, 1273, 1158, 448, 940, 136, 692, 884, 394, 840, 792, 257, 1236, 101, 311, 1160, 829, 744, 282, 37, 296, 1189, 712, 69, 691, 975, 496, 291, 360, 216, 796, 375, 1042, 706, 379, 1374, 76, 278, 472, 354, 958, 900, 21, 727, 569, 458, 658, 557, 487, 216, 601, 1138, 164, 151, 1102, 320, 170, 204, 424, 1375, 171, 476, 292, 298, 1117, 770, 760, 23, 278, 937, 1152, 848, 1199, 515, 751, 602, 798, 65, 216, 44, 1256, 1045, 732, 923, 20, 653, 595, 364, 976, 488, 1259, 174, 684, 840, 593, 1267, 632, 632, 659, 771, 1220, 649, 960, 972, 159, 248, 782, 35, 24, 1087, 395, 139, 73, 254, 696, 1150, 405, 1329, 144, 425, 603, 899, 1309, 241, 1126, 343, 785, 585, 1200, 299, 911, 1351, 336, 1084, 138, 1188, 1320, 534, 949, 69, 1222, 328, 1346, 349, 109, 321, 771, 265, 473, 709, 5, 1292, 654, 313, 601, 928, 680, 1017, 633, 272, 809, 510, 639, 939, 999, 178, 86, 54, 508, 208, 657, 63, 987, 1134, 1373, 685, 1041, 769, 466, 138, 407, 1065, 397, 541, 1188, 439, 512, 670, 370, 1199, 274, 1226, 1232, 415, 980, 376, 350, 417, 149, 346, 467, 1123, 448, 1377, 620, 584, 507, 857, 1304, 973, 969, 1157, 328, 394, 1115, 480, 554, 829, 1133, 293, 278, 855, 1030, 834, 1024, 1348, 90, 686, 685, 1063, 49, 1345, 533, 1338, 382, 208, 602, 1152]

if __name__ == '__main__':
  import sys
  fptr = sys.stdout

  n = int(input().strip())

  connection = list(map(int, input().rstrip().split()))

  result = rerouting(connection)

  fptr.write(str(result) + '\n')

  fptr.close()
  


