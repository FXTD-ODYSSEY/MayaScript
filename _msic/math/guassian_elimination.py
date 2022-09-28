# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/68994619/13452951
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-26 14:22:42"


import numpy as np
import time
import contextlib
import random

matrix_size = 2500
source = [[random.random() for j in range(matrix_size)] for i in range(matrix_size)]
# source = [
#     [0, 2, 12],
#     [3, 4, 19],
#     [4, 15, 24],
# ]
print(np.round(source, 3))


def inverse(matrix):
    matrix_len = len(matrix)  # defining the range through which loops will run

    # NOTES(timmyliang): 构建单位矩阵
    E_matrix = [
        [1.0 if i == j else 0.0 for i in range(matrix_len)] for j in range(matrix_len)
    ]

    # NOTES(timmyliang): 构建 [M|E] 矩阵
    for i in range(len(matrix)):
        matrix[i].extend(E_matrix[i])

    # print(np.round(matrix, 3))
    # print("start")
    # main loop for gaussian elimination begins here
    for ptnum in range(matrix_len):
        if abs(matrix[ptnum][ptnum]) < 1.0e-12:
            for i in range(ptnum + 1, matrix_len):
                if abs(matrix[i][ptnum]) > abs(matrix[ptnum][ptnum]):
                    for j in range(ptnum, 2 * matrix_len):
                        matrix[ptnum][j], matrix[i][j] = (
                            matrix[i][j],
                            matrix[ptnum][j],
                        )  # swapping of rows
                    break

        pivot = matrix[ptnum][ptnum]  # defining the pivot
        if pivot == 0:  # checking if matrix is invertible
            print("This matrix is not invertible.")
            return
        else:
            # print(np.round(matrix, 3))
            for j in range(ptnum, 2 * matrix_len):  # index of columns of the pivot row
                matrix[ptnum][j] /= pivot

            # print(np.round(matrix, 3))

            for i in range(matrix_len):  # index the subtracted rows
                # print(i,k,matrix[i][k])
                if i == ptnum or matrix[i][ptnum] == 0:
                    continue

                factor = matrix[i][ptnum]
                for j in range(ptnum, 2 * matrix_len):  # index the columns for subtraction
                    matrix[i][j] -= factor * matrix[ptnum][j]

            # print(np.round(matrix, 3))
            # print("================================")

            # if k > 1:
            #     break

    for row in range(matrix_len):  # displaying the matrix
        matrix[row] = matrix[row][matrix_len:]
    return matrix


@contextlib.contextmanager
def log_time(msg=""):
    curr = time.time()
    yield
    print(f"[{msg}]elapsed time: {time.time() - curr}")


with log_time("numpy"):
    numpy_res = np.round(np.linalg.inv(source), 3)

# with log_time("calc"):
#     calc_res = np.round(inverse(source), 3)

print(numpy_res)
# print(calc_res)
# print(np.round(numpy_res, 3) == np.round(calc_res, 3))
