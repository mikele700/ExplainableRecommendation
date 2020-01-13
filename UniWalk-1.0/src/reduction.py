# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 19:56:34 2020

@author: Michele
"""

import pandas as pd
from par import parse_args, set_paras, set_files, set_basic_info


if __name__ == '__main__':
    
	# 1. Get arguments
    args = parse_args()
    set_paras(args)
    set_files(args)
    set_basic_info(args)
    mode = 1
    
    if mode == 0:
        threshold = 10000
        names = ['user_id', 'item_id', 'rating']
        df = pd.read_csv("../data/%s/input/rating.tsv" % args.dataset, sep='\t', names=names)
        df = df.loc[df['user_id'] < threshold]
        df.to_csv("../data/%s/input/reducted_rating_%d.txt" % (args.dataset, threshold), sep='\t', header=False, index=False)
    elif mode == 1:
        threshold_rating = 20000
        threshold_link = 116258
        names = ['user_id', 'item_id', 'rating']
        rating = pd.read_csv("../data/%s/input/rating.txt" % args.dataset, sep='\t', names=names)
        names = ['node1', 'node2']
        link = pd.read_csv("../data/%s/input/link.txt" % args.dataset, sep='\t', names=names)
        rating = rating.loc[rating['user_id'] < threshold_rating]
        #link = link.loc[((link['node1'] < threshold_rating) | (link['node1'] > threshold_link)) & ((link['node2'] < threshold_rating) | (link['node2'] > threshold_link))]
        link = link.loc[((link['node1'] < threshold_rating) & (link['node2'] < threshold_rating))]
        rating.to_csv("../data/%s/input/reducted_rating_%d.txt" % (args.dataset, threshold_rating), sep='\t', header=False, index=False)
        link.to_csv("../data/%s/input/reducted_link_%d.txt" % (args.dataset, threshold_rating), sep='\t', header=False, index=False)
        
