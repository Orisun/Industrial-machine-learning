# coding=utf-8

import math

def dcg_at_k(rankArray, k):
    '''rank值越大表示越相关，rank最小值为0
    '''
    T = min(k, len(rankArray))
    assert T > 0
    rect = 0.0
    for i in xrange(T):
        rect += (math.pow(2.0, rankArray[i]) - 1) / math.log(2 + i, 2)
    return rect

def ndcg_at_k(rankArray, k):
    DCG = dcg_at_k(rankArray, k)
    maxDCG = dcg_at_k(sorted(rankArray, reverse=True), k)
    if maxDCG == 0:
        return 0
    NDCG = DCG / maxDCG
    return NDCG

rankArray = [5, 2, 4, 4, 4, 4, 3]
print ndcg_at_k(rankArray, k=5)