import numpy as np
import pandas as pd
import time
import sqlite3


data_home = './'

triplet_dataset = pd.read_csv(filepath_or_buffer = data_home + 'train_triplets.txt', sep = '\t', header = None, names = ['user', 'song', 'play_count'], nrows = 100000)


conn = sqlite3.connect(data_home + 'track_metadata.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
cur.fetchall()


track_metadata_df = pd.read_sql(con = conn, sql = 'select * from songs')
track_metadata_df = track_metadata_df.drop_duplicates(['song_id'])
track_metadata_df.shape
triplet_dataset.head()

del(track_metadata_df['track_id'])
del(track_metadata_df['artist_mbid'])
del(track_metadata_df['artist_id'])
del(track_metadata_df['duration'])
del(track_metadata_df['artist_familiarity'])
del(track_metadata_df['artist_hotttnesss'])
del(track_metadata_df['track_7digitalid'])
del(track_metadata_df['shs_perf'])
del(track_metadata_df['shs_work'])

triplet_dataset_merged = pd.merge(triplet_dataset, track_metadata_df, how='left', left_on='song', right_on='song_id')


#计算每个用户听歌的总次数
triplet_dataset_merged_res = triplet_dataset_merged[['user','play_count']].groupby('user').sum().reset_index()

triplet_dataset_merged_res.rename(columns={'play_count':'total_listen_count'},inplace=True)

triplet_dataset_merged_res.rename(columns={'listen_count':'total_listen_count'},inplace=True)
#计算结果join到triplet_dataset_merged
triplet_dataset_merged_result = pd.merge(triplet_dataset_merged,triplet_dataset_merged_res, how='left', on='user')
#计算得分
triplet_dataset_merged_result['fractional_play_count'] = triplet_dataset_merged_result['play_count']/triplet_dataset_merged_result['total_listen_count']

#重新定义
small_set = triplet_dataset_merged_result
#user与item分别去重后重新定义索引值
user_codes = small_set.user.drop_duplicates().reset_index()
song_codes = small_set.song.drop_duplicates().reset_index()
#重新命名
user_codes.rename(columns={'index':'user_index'}, inplace=True)
song_codes.rename(columns={'index':'song_index'}, inplace=True)

song_codes['so_index_value'] = list(song_codes.index)
user_codes['us_index_value'] = list(user_codes.index)
#将结果加入到small_set
small_set = pd.merge(small_set,song_codes,how='left')
small_set = pd.merge(small_set,user_codes,how='left')
#取出我们最终需要的数据进行转换
mat_candidate = small_set[['us_index_value','so_index_value','fractional_play_count']]

from scipy.sparse import coo_matrix
data_array = mat_candidate.fractional_play_count.values
row_array = mat_candidate.us_index_value.values
col_array = mat_candidate.so_index_value.values

data_sparse = coo_matrix((data_array, (row_array, col_array)),dtype=float)


#SVD
#导入相关包
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
def compute_estimated_matrix(urm, U, S, Vt, uTest, K, test):
    rightTerm = S*Vt
    max_recommendation = 250
    estimatedRatings = np.zeros(shape=(MAX_UID, MAX_PID), dtype=np.float16)
    recomendRatings = np.zeros(shape=(MAX_UID,max_recommendation ), dtype=np.float16)
    for userTest in uTest:
        prod = U[userTest, :]*rightTerm
        estimatedRatings[userTest, :] = prod.todense()#返回矩阵
        recomendRatings[userTest, :] = (-estimatedRatings[userTest, :]).argsort()[:max_recommendation]#找出从小到大排序的索引值（前面加了负号，即找出从大到小索引）
    return recomendRatings

K = 10
urm = data_sparse
MAX_PID = urm.shape[1]
MAX_UID = urm.shape[0]

U, S, Vt = compute_svd(urm, K)

uTest = [1,2,5,10,100,500,1000]
uTest_recommended_items = compute_estimated_matrix(urm, U, S, Vt, uTest, K, True)


def speed():
    for user in uTest:
        print("当前待推荐用户编号 {}". format(user))
        rank_value = 1
        for i in uTest_recommended_items[user,0:10]:
            song_details = small_set[small_set.so_index_value == i].drop_duplicates('so_index_value')[['title','artist_name']]
            print("推荐编号： {} 推荐歌曲： {} 作者： {}".format(rank_value, list(song_details['title'])[0],list(song_details['artist_name'])[0]))
            rank_value+=1

from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as pool:
    future = pool.submit(speed,)
