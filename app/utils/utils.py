from app.utils import get_small_set, get_data_sparse
import math as mt
from scipy.sparse.linalg import * #used for matrix multiplication
from scipy.sparse.linalg import svds
from scipy.sparse import csc_matrix
import pandas as pd
import numpy as np
import sqlite3
import time
from scipy.sparse import coo_matrix

small_set = get_small_set()
data_sparse = get_data_sparse()

def compute_svd(urm, k):
    u, s, v_t = svds(urm, k)
    dim = (len(s), len(s))
    s_1 = np.zeros(dim, dtype=np.float32)
    for i in range(0, len(s)):
        s_1[i, i] = mt.sqrt(s[i])

    u = csc_matrix(u, dtype=np.float32)
    s_1 = csc_matrix(s, dtype=np.float32)
    v_t = csc_matrix(v_t, dtype=np.float32)

    return u, s_1, v_t

def compute_estimated_matrix(U, S, Vt, uTest, uid, pid):
    right_term = S*Vt
    max_recommendation = 250
    estimated_ratings = np.zeros(shape=(uid, pid), dtype=np.float16)
    recommend_ratings = np.zeros(shape=(uid,max_recommendation ), dtype=np.float16)
    for userTest in uTest:
        prod = U[userTest, :]*right_term
        estimated_ratings[userTest, :] = prod.todense()#返回矩阵
        recommend_ratings[userTest, :] = (-estimated_ratings[userTest, :]).argsort()[:max_recommendation]#找出从小到大排序的索引值（前面加了负号，即找出从大到小索引）
    return recommend_ratings


def speed(users, recommend):
    for user in users:
        rank_value = 1
        res = []
        for i in recommend[user, 0:10]:
            song_details = small_set[small_set.so_index_value == i].drop_duplicates('so_index_value')[
                ['title', 'artist_name']]
            test = {
                'recommend_id': rank_value,
                'recommend_music': list(song_details['title'])[0],
                'artist': list(song_details['artist_name'])[0]
            }
            # print("推荐编号： {} 推荐歌曲： {} 作者： {}".format(rank_value, list(song_details['title'])[0],
            #                                         list(song_details['artist_name'])[0]))
            res.append(test)
            rank_value += 1
        return res