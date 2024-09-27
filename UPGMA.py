# lowest_cell:
#   Locates the smallest cell in the table
def lowest_cell(table):
    # Set default to infinity
    min_cell = float("inf")
    x, y = -1, -1

    # Go through every cell, looking for the lowest
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] < min_cell:
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


# join_table:
#   Joins the entries of a table on the cell (a, b) by averaging their data entries
def join_table(table, a, b, M_clusters):
    # Swap if the indices are not ordered
    if b < a:
        a, b = b, a

    # For the lower index, reconstruct the entire row (A, i), where i < A
    row = []
    for i in range(0, a):
        row.append((table[a][i] + table[b][i]) / 2)
    table[a] = row

    # Then, reconstruct the entire column (i, A), where i > A
    #   Note: Since the matrix is lower triangular, row b only contains values for indices < b
    for i in range(a + 1, b):
        table[i][a] = (table[i][a] * M_clusters[a] + table[b][i] * M_clusters[b]) / (
            M_clusters[a] + M_clusters[b]
        )

    #   We get the rest of the values from row i
    for i in range(b + 1, len(table)):
        table[i][a] = (table[i][a] * M_clusters[a] + table[i][b] * M_clusters[b]) / (
            M_clusters[a] + M_clusters[b]
        )
        # Remove the (now redundant) second index column entry
        del table[i][b]

    # Remove the (now redundant) second index row
    del table[b]


def add_cluster_counter(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = (table[i][j], 1)


# UPGMA:
#   Runs the UPGMA algorithm on a labelled table
def UPGMA(table, labels):
    # Until all labels have been joined...
    print(table)
    M_clusters = [1] * len(labels)
    print(M_clusters)
    # add_cluster_counter(table)

    while len(labels) > 1:
        # Locate lowest cell in the table
        x, y = lowest_cell(table)
        print("x: ", x, "y: ", y)

        # Join the table on the cell co-ordinates
        join_table(table, x, y, M_clusters)

        print(table)
        # Update the labels accordingly
        join_labels(labels, x, y, M_clusters)
        print(labels)
        print(M_clusters)
        print("_________________________")

    # Return the final label
    return labels[0]


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
    [0.12025698755638453],
    [0.30409883108112323, 0.30409883108112323],
    [0.5198603854199589, 0.5198603854199589, 0.35967981019641465],
    [0.4408399986765892, 0.18848582121067953, 0.5716050390351726, 0.8239592165010822],
]
print(UPGMA(M, M_labels))
# UPGMA(M, M_labels) should output: '((((A,D),((B,F),G)),C),E)'
