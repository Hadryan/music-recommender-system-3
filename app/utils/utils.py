import numpy as np
import pandas as pd
import time
import sqlite3
import math as mt
from scipy.sparse.linalg import * #used for matrix multiplication
from scipy.sparse.linalg import svds
from scipy.sparse import csc_matrix

#SVD求解
def compute_svd(urm, K):
    U, s, Vt = svds(urm, K)

    dim = (len(s), len(s))
    S = np.zeros(dim, dtype=np.float32)
    for i in range(0, len(s)):
        S[i,i] = mt.sqrt(s[i])

    U = csc_matrix(U, dtype=np.float32)
    S = csc_matrix(S, dtype=np.float32)
    Vt = csc_matrix(Vt, dtype=np.float32)

    return U, S, Vt

#构造结果数据
def compute_estimated_matrix(urm,MAX_UID, MAX_PID , U, S, Vt, uTest, K, test):
    rightTerm = S*Vt
    max_recommendation = 250
    estimatedRatings = np.zeros(shape=(MAX_UID, MAX_PID), dtype=np.float16)
    recomendRatings = np.zeros(shape=(MAX_UID,max_recommendation ), dtype=np.float16)
    for userTest in uTest:
        prod = U[userTest, :]*rightTerm
        estimatedRatings[userTest, :] = prod.todense()#返回矩阵
        recomendRatings[userTest, :] = (-estimatedRatings[userTest, :]).argsort()[:max_recommendation]#找出从小到大排序的索引值（前面加了负号，即找出从大到小索引）
    return recomendRatings

def speed(user, recommendList, smallSet):
    print("当前待推荐用户编号 {}".format(user))
    rank_value = 1
    for i in recommendList[user, 0:100]:
        song_details = smallSet[smallSet.so_index_value == i].drop_duplicates('so_index_value')[['title', 'artist_name']]
        print("推荐编号: {} 推荐歌曲: {} 作者: {}".format(rank_value, list(song_details['title'])[0], list(song_details['artist_name'])[0]))
        rank_value += 1