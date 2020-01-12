# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 14:09:59 2020

@author: Michele
"""
import pandas as pd
from sklearn.model_selection import StratifiedKFold

def xval(dataset, folds):
    names = ['user_id', 'item_id', 'rating']
    df = pd.read_csv("../data/%s/input/rating.tsv" % dataset, sep='\t', names=names, dtype='category')
    X = df[['user_id', 'item_id']]
    y = df[['rating']]
    skf = StratifiedKFold(n_splits=folds, shuffle=True)
    i = 0
    for train_index, test_index in skf.split(X, y):
        train = df.iloc[train_index]
        test = df.iloc[test_index]
        train.to_csv("../data/%s/input/train%d.csv" % (dataset, i), sep='\t', header=False, index=False)
        test.to_csv("../data/%s/input/test%d.csv" % (dataset, i), sep='\t', header=False, index=False)
        i += 1