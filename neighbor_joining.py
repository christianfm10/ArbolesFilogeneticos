# A Quick Implementation of UPGMA (Unweighted Pair Group Method with Arithmetic Mean)


# lowest_cell:
#   Locates the smallest cell in the table
def lowest_cell(table):
    # Set default to infinity
    min_cell = float("inf")
    x, y = -1, -1

    # Go through every cell, looking for the lowest
    for i in range(len(table)):
        for j in range(len(table[i])):
            # WARNING: I changed the < to <=
            if table[i][j] <= min_cell:
                min_cell = table[i][j]
                x, y = i, j

    # Return the x, y co-ordinate of cell
    return x, y


# join_labels:
#   Combines two labels in a list of labels
def join_labels(labels, a, b, M_clusters):
    # Swap if the indices are not ordered
    if b < a:
        a, b = b, a

    # Join the labels in the first index
    labels[a] = "(" + labels[a] + "," + labels[b] + ")"
    M_clusters[a] = M_clusters[a] + 1

    # Remove the (now redundant) label in the second index
    del M_clusters[b]
    del labels[b]


def add_cluster_counter(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = (table[i][j], 1)


def get_sum_row(table):
    sum_rows_arr = [0] * len(table)

    # Sumar los elementos de la parte triangular inferior
    for i in range(len(table)):
        sum_rows_arr[i] += sum(table[i])  # Sumar los elementos de la fila "i"

    # Sumar los elementos correspondientes de la parte superior (espejo de la triangular inferior)
    for i in range(1, len(table)):  # Empezar desde la segunda fila
        for j in range(len(table[i])):
            sum_rows_arr[j] += table[i][j]  # Sumar los elementos espejo

    return sum_rows_arr


def get_min_pair_seq(table, sum_rows_arr):
    N_2 = len(table) - 2
    M = []
    for i in range(len(table)):
        row = []
        for j in range(len(table[i])):
            # if i == j:
            # M.append([])
            row.append(N_2 * table[i][j] - (sum_rows_arr[j] + sum_rows_arr[i]))
        M.append(row)
    print(M)
    print(lowest_cell(M))
    return lowest_cell(M)


def join_neighbors(table, sum_rows_arr, x, y):
    N_2 = len(table) - 2
    print("table", table)
    print("len:", len(table))
    print("N_2 :", N_2)

    # print(table[x][y])
    print(x, y)
    # print(sum_rows_arr[x], sum_rows_arr[y])
    # NOTE: Here I swap x and y
    distance1 = 0.5 * (table[x][y] + (sum_rows_arr[y] - sum_rows_arr[x]) / N_2)
    distance2 = table[x][y] - distance1

    i_j = []
    for Y in range(len(table)):
        i, j = x, y
        Y2 = Y
        if Y > i:
            i, Y = Y, i
        if Y2 > x:
            j, Y2 = Y2, j
        print("i: ", i)
        print("j: ", j)
        print("Y: ", Y)
        if Y != i and Y != j:
            b_Yk = 0.5 * (table[i][Y] + table[j][Y2] - table[x][y])
            i_j.append(b_Yk)
            # print("b_Yk")
            # print(b_Yk)
        # print("hollaaa")
    table.append(i_j)
    del table[x]
    del table[y]
    print("table")
    print(table)
    print("distance 1:", distance1, "distance 2:", distance2)


def nj(table):
    while len(table) > 2:
        sum_rows_arr = get_sum_row(table)
        print(sum_rows_arr)
        x, y = get_min_pair_seq(table, sum_rows_arr)
        join_neighbors(table, sum_rows_arr, x, y)

        print("__________________________________________________")


## A test using an example calculation from http://www.nmsr.org/upgma.htm


# alpha_labels:
#   Makes labels from a starting letter to an ending letter
def alpha_labels(start, end):
    labels = []
    for i in range(ord(start), ord(end) + 1):
        labels.append(chr(i))
    return labels


# Test table data and corresponding labels
# M_labels = alpha_labels("A", "D")  # A through G
M_labels = ["A", "B", "C", "D", "E"]
M = [
    [],  # A
    [8],  # B
    [7, 9],  # C
    [12, 14, 11],  # D
    #    [33, 36, 41, 31],           #E
    #    [18, 1, 32, 17, 35],        #F
    #    [13, 13, 29, 14, 28, 12]    #G
]
M = [[], [17], [21, 30], [31, 34, 28], [23, 21, 39, 43]]
M = [
    [],
    [5],
    [4, 5],
    [9, 10, 7],
    [8, 9, 6, 7],
]

M = [
    [],
    [0.12025698755638453],
    [0.30409883108112323, 0.30409883108112323],
    [0.5198603854199589, 0.5198603854199589, 0.35967981019641465],
    [0.4408399986765892, 0.18848582121067953, 0.5716050390351726, 0.8239592165010822],
]

"""
[
    [],
    [5],
    [4, 5],
    [5, 6, 3],
]
"""
# print(sum_matrix_inferior(M))
print(nj(M))
# print(UPGMA(M, M_labels))
# UPGMA(M, M_labels) should output: '((((A,D),((B,F),G)),C),E)'
