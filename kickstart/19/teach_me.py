# Input template
try:
    input = raw_input
except NameError:
    pass

def read_int():
  return int(input())

def read_ints():
  return [int(i) for i in input().split()]

def read_int_arr():
  return list(map(int, input().split()))

def explode(s):
  return [ch for ch in s]

def read_input():
  num_cases = int(input())
  for t in range(1, num_cases+1):
    N, S = read_ints()
    skills_per_person = [read_int_arr()[1:] for _ in range(N)]
    res = solve(N, S, skills_per_person)
    print("Case #{}: {}".format(t, res))

# Solution begins here
def solve(N, S, skills_per_person):
  from collections import defaultdict
  skill_owners = [set() for _ in range(S)]
  for person, skills in enumerate(skills_per_person):
    for s in skills:
      skill_owners[s-1].add(person)
  universe = set(range(N))
  emeritus = set()
  alums = set()
  count = 0
  for skill, teachers in enumerate(skill_owners):
    if len(teachers) > 0:
      new_teachers = teachers - emeritus
      students = (universe - teachers)
      new_students = students - alums
      count += len(new_teachers) * len(students) + len(teachers) * len(new_students)
      emeritus |= teachers
      alums |= students
  return count

if __name__ == "__main__":
  # read_input()
  solve(4, 100, [[80, 90, 100, 5], [90], [80], [80, 90, 100]])







if __name__ == "__main__":
  read_input()