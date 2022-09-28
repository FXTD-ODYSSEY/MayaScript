# -*- coding: utf-8 -*-
"""
https://blog.csdn.net/cauchy7203/article/details/114460279
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-09-27 16:43:23'



import sys
import numpy as np

n = 5
a = np.round(np.random.rand(n,n)*10-5,3)
for row in range(n):
    for col in range(n):
        a[row][col] = 0 
I = np.eye(n)

A = a.copy()

for i in range(n):
  if A[i][i] == 0.0:
    sys.exit('Divide by zero detected!')
      
  for j in range(n):
    if i != j:
      ratio = A[j][i]/A[i][i]

      for k in range(n):
        A[j][k] = A[j][k] - ratio * A[i][k]
        I[j][k] = I[j][k] - ratio * I[i][k]

for i in range(n):
  divisor = A[i][i]
  for j in range(n):
    A[i][j] = A[i][j]/divisor
    I[i][j] = I[i][j]/divisor

print('原矩阵：\r\n',a)
print('\r\n')

print('变换后的矩阵 A：\r\n',np.round(A,3))
print('\r\n')

print('逆矩阵 I：\r\n',np.round(I,3))
print('\r\n')

print(np.round(np.linalg.inv(a),3))
