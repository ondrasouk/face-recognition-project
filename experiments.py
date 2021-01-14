import numpy as np
matA = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
matB = [[2,2],[2,2],[2,2]]
def corner_matrix_combine(matA,matB):
    # Take matrix A and to its corned place matB
    # Use right bottom corner
    A_row = len(matA)
    B_row = len(matB)
    row_len = len(matB[0])

    for r in range(A_row - B_row, A_row):
        b_idx = r + B_row - A_row
        this_row = matA[r]
        add_row = matB[b_idx]
        this_row[-row_len:] = add_row[:]
        matA[r] = this_row
    return matA