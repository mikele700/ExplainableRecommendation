"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
- walk.py
  : generate random walks

This software is free of charge under research purposes.
For commercial purposes, please contact the authors.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Import packages
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Walk on each node
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def do_walk(args, g, transition_dict, sampling):
	# Arguments
	wl = args.wl

	# Ready to walk
	walks = list()
	nodes = g.nodes()

	# Make a random order of nodes to start
	np.random.shuffle(nodes)

	# Sample node lists from a start node
	for starter in nodes:
		# Sample a walk
		walk = get_random_walk(g, starter, wl, sampling, transition_dict, args)

		# Append the walk
		walks.append(walk)
		
	return walks



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Get random walk
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_random_walk(g, starter, walk_length, sampling, transition_dict, args):
	# Ready to walk
	curr = starter
	walk = [starter]
	# restart_prob = args.c

	# Random walk with restart
	for i in range(walk_length):
		# Get information of neighbors
		curr_neighbors_weight = g.neighbor_weights(curr)
		curr_neighbors = g.neighbor_indices(curr)

		if sampling == 'positive':
			curr_cumulate_bucket = transition_dict[curr]
			next_nth = get_positive_next_node(curr_cumulate_bucket, curr_neighbors_weight)
		elif sampling == 'negative':
			next_nth = get_negative_next_node(curr_neighbors_weight, args)
		elif sampling == 'unweighted':
			next_nth = get_unweighted_next_node(curr_neighbors)
		next_node = curr_neighbors[next_nth]
		
		# Fill walk and weight list
		walk.append(next_node)

		# Go to the next step
		curr = next_node
	
	return walk



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Get the next transition node
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 0. Under the positive random walk
def get_positive_next_node(curr_cumulate_bucket, curr_neighbors_weight):
	
	# Get random value in range cummulated sum
	unnormalized_sum = sum(curr_neighbors_weight)
	rand_val = np.random.rand() * unnormalized_sum

	# Get next node's position and weight
	n_th = np.searchsorted(curr_cumulate_bucket, rand_val) - 1

	return n_th

# 1. Under the negative random walk # MAY NOT BE USED LATER
def get_negative_next_node(curr_neighbors_weight, args):

	# Get rating information
	maxR = args.max_r
	minR = args.min_r

	# Get cummulated bucket
	reverser = (lambda x: maxR + minR - x)
	reversed_neigh_weight = list(map(reverser, curr_neighbors_weight))
	unnormalized_sum = sum(reversed_neigh_weight)
	bucket = [0]
	cummulate = 0
	for w in reversed_neigh_weight:
		cummulate = cummulate + w
		bucket.append(cummulate)

	# Get random value in range cummulated sum
	rand_val = np.random.rand() * unnormalized_sum

	# Get next node's position and weight
	n_th = np.searchsorted(bucket, rand_val) - 1

	return n_th

# 2. Under the unweighted random walk
def get_unweighted_next_node(curr_neighbors):
	total_num = len(curr_neighbors)
	rand_val = np.random.rand() * total_num
	n_th = int(rand_val)
	if n_th == total_num:
		n_th -= 1

	return n_th


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Additional function
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def is_u(x, min_u_id, max_u_id):
	return x >= min_u_id and x <= max_u_id

def do_restart(restart_prob):
	p = np.random.random()
	if p < restart_prob:
		return True
	else:
		return False
