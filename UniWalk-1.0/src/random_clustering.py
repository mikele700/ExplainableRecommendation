# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 21:16:45 2020

@author: Michele
"""
from par import parse_args, set_paras, set_files, set_basic_info
import random

if __name__ == '__main__':
    
    args = parse_args()
    set_paras(args)
    set_files(args)
    set_basic_info(args)
    
    profile_filename = "../data/%s/input/random_profile.txt" % (args.dataset)
    with open(profile_filename, mode='w') as f:
        for i in range(args.max_u_id + 1):
            f.write("%d\n" %random.randint(0,4))