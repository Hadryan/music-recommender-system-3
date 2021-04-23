from app.utils import get_data_sparse
from app.utils.utils import compute_svd, compute_estimated_matrix, speed
from flask import jsonify
from app.api import bp

import pandas as pd
import numpy as np
import sqlite3
import time
from scipy.sparse import coo_matrix

data_sparse = get_data_sparse()

k = 10
urm = data_sparse
max_pid = urm.shape[1]
max_uid = urm.shape[0]

u, s, v =compute_svd(urm, k)
uTest = [1, 2, 5, 10, 100, 500, 1000]
user_recommend_list = compute_estimated_matrix(u,s, v, uTest, max_uid, max_pid)
#
# @bp.route('/music', methods=['GET'])
# def test():
#     return jsonify('music')
