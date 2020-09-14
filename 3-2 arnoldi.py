#!/usr/bin/env pyton
# coding=utf-8
 
import numpy as np

class SparseMatrix():
    '''用dict实现高度稀疏的矩阵，dict的key是元素在matrix中的二维坐标，dict的value是元素的值
    '''
    def __init__(self):
        self.arr = {}
 
    def get(self, row, col):
        key = (row, col)
        if key in self.arr:
            return self.arr[key]
        else:
            return 0
 
    def set(self, row, col, value):
        key = (row, col)
        self.arr[key] = value
 
    def mul(self, vec):
        '''与一个一维向量相乘，返回一个list
        '''
        length = len(vec)
        rect = [0] * length
        for k, v in self.arr.items():
            i = k[0]
            j = k[1]
            rect[i] += v * vec[j]
        return rect
 
    def mulMatrixCol(self, matrix, col):
        '''与矩阵的第col列相乘,返回一个n*1的矩阵
        '''
        length = matrix.shape[0]
        rect = np.zeros((length, 1))
        for k, v in self.arr.items():
            i = k[0]
            j = k[1]
            rect[i, 0] += v * matrix[j, col]
        return rect
 
    def mulMatrix(self, matrix):
        '''与一个矩阵相乘
        '''
        col_num = matrix.shape[1]
        rect = self.mulMatrixCol(matrix, 0)
        for i in range(1,col_num):
            rect = np.hstack((rect, self.mulMatrixCol(matrix, i)))
        return rect
 
    def transmul(self, vec):
        '''矩阵转置后与一维向量相乘
        '''
        length = len(vec)
        rect = [0] * length
        for k, v in self.arr.items():
            i = k[1]
            j = k[0]
            rect[i] += v * vec[i]
        return rect
 
def arnoldi_iteration(Q, n, alpha):
    '''
    对Q进行分解，QV=VH。
    Q是输入参数，numpy.matrix类型，n行n列。
    V和H都是输出参数，numpy.matrix类型。
    V是n行r+1列，每列模长为1且各列正交。V的转置与逆相等。
    H是r+1行r列的上三角矩阵。
    alpha用于限制循环次数，alpha设置得要大于Q的秩。
    '''
    if alpha > n or alpha <= 0:
        alpha = n
    V = np.zeros((n, 1))
    V[0, 0] = 1
    h_col_list=[]
    k = 1
    while k <= alpha:
        h_col = []
        v_k = Q.mulMatrixCol(V,k-1)
        for j in range(k):
            product = np.dot(np.matrix(V[:,j]).reshape(n,1).transpose(), v_k)[0,0]
            h_col.append(product)
            v_k = v_k - product * (np.matrix(V[:,j]).reshape(n,1))
        norm2 = np.linalg.norm(v_k, ord=2)
        if norm2 == 0:
            print "norm2=0, will break"
            break
        h_col.append(norm2)
        h_col_list.append(h_col)
        v_k = v_k / norm2
        V = np.hstack((V, np.matrix(v_k)))
        k += 1
    r = len(h_col_list)
    H = np.zeros((r, r))
    for i in range(r):
        h_col = h_col_list[i]
        for j in range(len(h_col)):
                if j < r:
                    H[j, i] = h_col[j]
    V = V[:, :r]
    return (V, H)
 
if __name__ == '__main__':
    Q=SparseMatrix()
    Q.set(0,1,0.5)
    Q.set(0,2,1)
    Q.set(1,0,0.5)
    Q.set(1,3,1)
    Q.set(2,0,0.5)
    Q.set(3,1,0.5)
    (V,H)=arnoldi_iteration(Q,4,-1)
    print "V="
    print V
    print "H="
    print H
    print "VHV^T="
    print np.dot(np.dot(V,H),V.transpose())
    print "QV="
    print Q.mulMatrix(V)
    print "VH="
    print np.dot(V,H)
