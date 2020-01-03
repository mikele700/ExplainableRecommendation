"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Uniwalk
- An explainable and accurate recommender system
  for rating and network data

Authors
- Haekyu Park (hkpark627@snu.ac.kr)
- Hyunsik Jeon (jeon185@gmail.com)
- Junghwan Kim (kjh900809@snu.ac.kr)
- Beunguk Ahn (elaborate@snu.ac.kr)
- U Kang (ukang@snu.ac.kr)

File
- build_graph.py
  : generates a unified graph that merges ratings and
    a social network.

This software is free of charge under research purposes.
For commercial purposes, please contact the authors.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Import packages
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Build graph structure with rating and trust information
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def build_graph(args, numfolds):
	# Set parameters
	maxR = args.max_r
	minR = args.min_r
	
	# Read ratings
	header = ['u', 'i', 'r']
	buckets = list()
	for fold in range(numfolds):
		input_rating = args.inputpath + "b%d.csv" % fold
		buckets.append(pd.read_csv(input_rating, sep='\t', names=header))

	# For all folds
	for fold in range(numfolds):
		# 0. Get ratings
		train = pd.DataFrame()
		for i, b in enumerate(buckets):
			if i != fold:
				train = pd.concat([train, b])
		num_rating = len(train.r)

		# 1. Read trust network
		uu_header = ['u1', 'u2', 'w']
		network = pd.read_csv(args.inputpath + "link.tsv", sep='\t', names=uu_header)
		num_uu_links = network.shape[0]

		# 2. Complete user-item weights
		ui_weights = coo_matrix((np.zeros(num_rating), (train.u, train.i)))
		for j, r in enumerate(train.r):
				ui_weights.data[j] = r

		# 3. Complete user-user weights
		uu_weights = coo_matrix((np.zeros(num_uu_links), (network.u1, network.u2)))
		for j in range(num_uu_links):
				uu_weights.data[j] = args.c

		# 4. Set filepaths	
		p_graph_filename = args.graphpath + "p_graph_%s_%d.txt" % (args.graphparas, fold)
		n_graph_filename = args.graphpath + "n_graph_%s_%d.txt" % (args.graphparas, fold)
		
		# 5. Save graph
		with open(p_graph_filename, mode='w') as f:
			# Save uu edges
			for u1, u2, w in zip(uu_weights.row, uu_weights.col, uu_weights.data):
				f.write("%d\t%d\t%.1f\n" % (u1, u2, w))
				f.write("%d\t%d\t%.1f\n" % (u2, u1, w))

			# Save ui edges
			for u, i, w in zip(ui_weights.row, ui_weights.col, ui_weights.data):
				f.write("%d\t%d\t%.1f\n" % (u, i, w))
				f.write("%d\t%d\t%.1f\n" % (i, u, w))

		with open(n_graph_filename, mode='w') as f:
			# Save uu edges
			for u1, u2, w in zip(uu_weights.row, uu_weights.col, uu_weights.data):
				f.write("%d\t%d\t%.1f\n" % (u1, u2, maxR + minR - w))
				f.write("%d\t%d\t%.1f\n" % (u2, u1, maxR + minR - w))

			# Save ui edges
			for u, i, w in zip(ui_weights.row, ui_weights.col, ui_weights.data):
				f.write("%d\t%d\t%.1f\n" % (u, i, w))
				f.write("%d\t%d\t%.1f\n" % (i, u, w))

		print("%s is made" % p_graph_filename)
		print("%s is made" % n_graph_filename)
