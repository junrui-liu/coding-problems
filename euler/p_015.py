def lattice(n):
    def taxicab_distance(a, b):
        ax, ay = a
        bx, by = b
        return abs(ax-bx) + abs(ay-by)

    matrix = [[0 for j in range(n+1)] for i in range(n+1)]
    points = [(i, j, taxicab_distance((i,j), (n,n))) \
                for j in range(n+1) for i in range(n+1)]
    matrix[n][n] = 1

    for k in range(1, 2*n + 1):
        diagonal_entries = [(i,j) for (i,j,d) in points if d == k]
        for (x,y) in diagonal_entries:
            if x != n:
                matrix[x][y] += matrix[x+1][y]
            if y != n:
                matrix[x][y] += matrix[x][y+1]
    return matrix[0][0]


def lattice_fast(n):
    def factorial(n):
        product = 1
        while n > 0:
            product *= n
            n -= 1
        return product
    
    def binom(n, k):
        return factorial(n) // (factorial(n-k)*factorial(k))

    return binom(2*(n-1), n-1)