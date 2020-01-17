# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:14:17 2020

@author: Michele
"""

import pandas as pd
from sklearn.model_selection import train_test_split

def holdout(dataset, fold):
    names = ['user_id', 'item_id', 'rating']
    df = pd.read_csv("../data/%s/input/esempio.tsv" % dataset, sep='\t', names=names, dtype='category')
    train, test = train_test_split(df, test_size=0.2, random_state=10, shuffle=True, stratify=df['rating'])
    train.to_csv("../data/%s/input/train%d.csv" % (dataset, fold), sep='\t', header=False, index=False)
    test.to_csv("../data/%s/input/test%d.csv" % (dataset, fold), sep='\t', header=False, index=False)