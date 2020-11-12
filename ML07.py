# -*- coding: utf-8 -*-
# モデルの保存
# APIなどで利用する際はjoblib.loadで保存したモデルを読み込んで、
# 入力されたデータに対してpredictを行えば良い
import numpy as np
from ML04 import get_stock
import pandas as pd
from sklearn import tree
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

def get_params(ccode, last_date, db):
    '''
    決定木に最適なパラメーターを総当たりで取得します。
    '''
    _top_mean = 0
    _data_length = 0
    _step = 0
    _min_samples_leaf = 0
    _max_depth = 0
    for data_length in range(30, 40, 10):
        for step in range(4, 12):
            for min_samples_leaf in range(1, 7):
                for max_depth in range(2, 8):
                    clf, train_X, train_y = lean(ccode, last_date, db, data_length, step, min_samples_leaf, max_depth)
                    scores = cross_val_score(clf, train_X, train_y, cv=5)
                    mean = scores.mean()
                    del clf
                    if _top_mean < mean:
                        _top_mean = mean
                        _data_length = data_length
                        _step = step
                        _min_samples_leaf = min_samples_leaf
                        _max_depth = max_depth
#     print("{}%, length:{}, step:{}, leaf: {}, depth: {}".format(int(_top_mean * 100), _data_length, _step, _min_samples_leaf, _max_depth))
    return _top_mean, _data_length, _step, _min_samples_leaf, _max_depth