# coding=utf-8
__author__ = "orisun"

import numpy as np
 
EPS = 1.0e-9
 
'''实现3种初等行变换'''
def swapRow(A, i, j):
    '''交换矩阵A的第i行和第j行'''
    n = A.shape[1]
    for x in xrange(n):
        tmp = A[i, x]
        A[i, x] = A[j, x]
        A[j, x] = tmp
 
def scaleRow(A, i, coef):
    '''矩阵A的第i行元素乘以一个非0系数coef'''
    assert abs(coef) > EPS
    n = A.shape[0]
    for x in xrange(n):
        A[i, x] *= coef
 
def addRowToAnother(A, i, j, coef):
    '''把矩阵A第i行的coef倍加到第j行上去'''
    assert abs(coef) > EPS
    n = A.shape[0]
    for x in xrange(n):
        A[j, x] = coef * A[i, x] + A[j, x]
 
def gauss_jordan(A, column_pivot=True):
    '''高斯-约旦法求矩阵的逆。
       参数column_pivot为True时将采用列主元消去法。该方法经了优化，不需要额外的内存空间来存储增广矩阵。但是会改变原始的输入矩阵A，最终A变成了它自身的逆。由于没有增广矩阵，计算量至少减少为原来的一半。时间复杂度为O(n^3)
    '''
    n = A.shape[0]
    for pivot in xrange(n):
        # 构建n行1列的B矩阵，它的第pivot行上为1，其他全为0
        B = np.array([[0.0] * n]).T
        B[pivot, 0] = 1.0
        if column_pivot:
            # 寻找第pivot列绝对值最大的元素（即列主元），把该元素所在的行与第pivot行进行交换
            if(pivot < n - 1):
                maxrow = pivot
                maxval = abs(A[pivot, pivot])
                for row in xrange(pivot + 1, n):  # 只需要从该列的第pivot个元素开始往下找
                    val = abs(A[row, pivot])
                    if(val > maxval):
                        maxval = val
                        maxrow = row
                if(maxrow != pivot):
                    swapRow(A, pivot, maxrow)
                    swapRow(B, pivot, maxrow)
 
        # 第pivot行乘以一个系数，使得A[pivot,pivot]变为1
        coef = 1.0 / A[pivot, pivot]
        if abs(coef) > EPS:
            for col in xrange(0,  n):
                A[pivot, col] *= coef
            B[pivot, 0] *= coef
 
        # 把第pivot行的N倍加到其他行上去，使得第pivot列上除了A[pivot,pivot]外其他元素都变成0
        for row in xrange(n):
            if row == pivot:
                continue
            coef = 1.0 * A[row, pivot]
            if abs(coef) > EPS:
                for col in xrange(0, n):
                    A[row, col] -= coef * A[pivot, col]
                B[row, 0] -= coef * B[pivot, 0]
 
        # 把B存储到A的第pivot列上去
        for row in xrange(n):
            A[row, pivot] = B[row, 0]
 
    # 此时的A已变成了原A的逆
    return A

def test():
    import time
    from numpy import random
    from scipy import linalg
    import math
 
    n = 100    #n上千时用就不适合用gauss_jordan法了，半天算不出结果
    arr = random.randint(100, size=(n, n))
    begin = time.time()
    gauss_jordan(arr, False)
    end = time.time()
    print 'gauss_jordan use time ', end - begin
    # 矩阵规模很小时gauss_jordan法更快。矩阵规模稍大时linalg.inv更快。
    # begin = time.time()
    # linalg.inv(arr)       #使用linalg.inv经常无法求解，因为随机构造出来的矩阵经常是奇异矩阵
    # end = time.time()
    # print 'linalg.inv use time ', end - begin
 
 
if __name__ == '__main__':
    test()
 
    print "original"
    A = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]], dtype='d')
    print A
 
    print "inverse matrix"
    print gauss_jordan_0(A, True)
 
    print "inverse matrix"
    print gauss_jordan(A, True)
 
    print "swap row1 and row2"
    swapRow(A, 1, 2)
    print A
 
    print "row1 multiple by -0.5"
    scaleRow(A, 1, -0.5)
    print A