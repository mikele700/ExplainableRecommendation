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
- embedding.py
  : learns biases and vectors of entities.

This software is free of charge under research purposes.
For commercial purposes, please contact the authors.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Import packages
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import pandas as pd
import graph as graph
from scipy.sparse import coo_matrix



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Read input
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Read training set
def read_train_ratings(args, fold):
	train = pd.DataFrame()
	for f in range(5):
		input_filename = args.inputpath + 'b%d.csv' % f 
		b = pd.read_csv(input_filename, sep='\t', names=['u', 'i', 'r'])
		if f != fold:
			train = pd.concat([train, b])
	return train


# Read test set
def read_test_ratings(args, fold):
	test = pd.DataFrame()
	input_filename = args.inputpath + 'b%d.csv' % fold
	test = pd.read_csv(input_filename, sep='\t', names=['u', 'i', 'r'])
	return test
	

# Read the unified graph
def read_graph(edge_filename):
	print("Read %s" % edge_filename)

	# Read undirected and weighted graph
	df = pd.read_csv(edge_filename, delimiter='\t', names=['e1', 'e2', 'w'])
	loaded_graph = coo_matrix((df.w, (df.e1, df.e2)))
	loaded_graph.tocsr()

	# return the loaded graph
	return graph.Graph(loaded_graph)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Initializer
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Initialize factors
def init_learn(args):
	a = np.sqrt((args.max_r + args.min_r) / args.dim) 
	Z = (np.random.random((args.num_entities, args.dim))) * a
	B = (np.random.random(args.num_entities)) * (a / 2)
	Dp = list()
	for i in range(args.max_i_id + 1):
		Dp.append(list())
	return B, Z, Dp


# Make transition table, whose key is a node,
#  and value is cumulative weights to neighbors
def make_transit(args, g):
	transition_dict = dict()
	nodes = g.nodes()
	id_to_th = {j: i for i, j in enumerate(nodes)}
	for curr in nodes:
		# Ready
		curr_neighbors_weight = g.neighbor_weights(curr)
		bucket = np.zeros(len(curr_neighbors_weight))

		# Get cummulated bucket
		cummulate = 0
		for transit_iter, w in enumerate(curr_neighbors_weight):
			cummulate += w
			bucket[transit_iter] = cummulate

		# Add bucket
		transition_dict[curr] = bucket
	
	return id_to_th, transition_dict

