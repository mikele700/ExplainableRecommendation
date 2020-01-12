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
    
    threshold = 10000
    names = ['user_id', 'item_id', 'rating']
    df = pd.read_csv("../data/%s/input/rating.tsv" % args.dataset, sep='\t', names=names)
    df = df.loc[df['user_id'] < threshold]
    df.to_csv("../data/%s/input/reducted_rating_%d.txt" % (args.dataset, threshold), sep='\t', header=False, index=False)
