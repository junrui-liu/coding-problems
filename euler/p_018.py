import sys

def parse_triangle_file(filename):
    triangle = []
    with open(filename, "r") as infile:
        for line in infile:
            triangle.append([int(d) for d in line.split()])
    return triangle


def solve(triangle):
    def get_parent(p):
        px, py = p
        return routes[px][py]
    # Each row is a list of (parent_entry, running sum) pairs
    routes = []
    routes.append([(None, triangle[0][0])])
    for i in range(1, len(triangle)):
        routes_row = []
        num_children = i + 1
        for j in range(num_children):
            current_val = triangle[i][j]
            left_parent = (i-1, j-1)
            right_parent = (i-1, j)
            if j > 0:
                _, left_sum = get_parent(left_parent)
                left_sum += current_val
            if j < num_children - 1:
                _, right_sum = get_parent(right_parent)
                right_sum += current_val
            # Left-most child,
            # so only one possible route from the right parent
            if j == 0:
                routes_row.append((right_parent, right_sum))
            # Right-most child,
            # so only one possible route from the left parent
            elif j == num_children - 1:
                routes_row.append((left_parent, left_sum))
            # Compare routes from left & right parrents
            else:
                if left_sum >= right_sum:
                    routes_row.append((left_parent, left_sum))
                else:
                    routes_row.append((right_parent, right_sum))
        routes.append(routes_row)
    return routes


if __name__ == "__main__":
    triangle = parse_triangle_file(sys.argv[1])
    routes = solve(triangle)
    parent, best_sum = max(routes[-1], key=lambda pair: pair[1])
    parents = list()
    sum_backtrace = best_sum
    while parent:
        p_row, p_col = parent
        parent_val = triangle[p_row][p_col]
        parents.append(parent_val)
        sum_backtrace -= parent_val
        parent, _ = routes[p_row][p_col]
    parents = parents[::-1] + [sum_backtrace]
    print(parents)
    print(best_sum)






