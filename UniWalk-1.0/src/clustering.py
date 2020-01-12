# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 18:13:56 2020

@author: Michele
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing
from par import parse_args, set_paras, set_files, set_basic_info
from sklearn.metrics import silhouette_samples, silhouette_score

if __name__ == '__main__':
	# 1. Get arguments
    args = parse_args()
    set_paras(args)
    set_files(args)
    set_basic_info(args)

    dataset_filename = "../data/%s/review/dataset.txt" %args.dataset
    df = pd.read_csv(dataset_filename, delimiter='\t')
    X = df[['Extra', 'Emoti', 'Agree', 'Consc', 'Openn']]
    X = preprocessing.normalize(X)
    kmeans = KMeans(n_clusters=10, random_state=0).fit(X)
    df['Label'] = kmeans.labels_
    silhouette_avg = silhouette_score(X, kmeans.labels_)
    print(silhouette_avg)