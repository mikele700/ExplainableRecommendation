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
- graph.py
  : defines graph

This software is free of charge under research purposes.
For commercial purposes, please contact the authors.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import numpy as np

class Graph:
	def __init__(self, coo_mat):
		self.coo = coo_mat
		self.lil = coo_mat.tolil()
		self.lil_t = coo_mat.transpose().tolil()

	# Get adjacent array of the graph
	def adj(self):
		return self.coo.toarray()

	# Return the number of nodes in the graph
	def number_of_nodes(self):
		return len(np.unique(self.coo.row))

	# Return the number of edges in the graph
	def number_of_edges(self):
		return int(len(self.coo.row) / 2)

	# Return nodes in the graph
	def nodes(self):
		return np.unique(self.coo.row)

	# Get neighbors of a node
	def neighbor_indices(self, node_num):
		return self.lil.rows[node_num]

	# Get adjacanet weights of a node
	def neighbor_weights(self, node_num):
		return self.lil.data[node_num]

	# Get the number of neighbors of a node
	def num_neighbors(self, node_num):
		return len(self.neighbor_indices(node_num))

	# Get iteration of edges
	def edges_iter(self):
		return zip(self.coo.row, self.coo.col, self.coo.data)

	# Change values of the graph
	def change_value(self, data_ith, value):
		self.coo.data[data_ith] = value

	# Get neighbors
	def in_neighbor_indices(self, node_num):
		return self.lil_t.rows[node_num]

	# Get weight between nodes
	def weight_bw_nodes(self, node1, node2):
		node1_neighbor = self.neighbor_indices(node1)
		nth = np.searchsorted(node1_neighbor, node2)
		node1_neighbor_weights = self.neighbor_weights(node1)
		return node1_neighbor_weights[nth]

	# Get half graph
	def get_half_row_col_data(self):
		g = self.coo
		entire_row = g.row
		entire_col = g.col
		entire_data = g.data
		half_row = list()
		half_col = list()
		half_data = list()
		entry_list = list()
		for i, (r, c, d) in enumerate(zip(entire_row, entire_col, entire_data)):
			if (r, c) in entry_list or (c, r) in entry_list:
				continue
			entry_list.append((r, c))
			half_row.append(r)
			half_col.append(c)
			half_data.append(d)
		return half_row, half_col, half_data

	# Return if the nodes are connected
	def connected(self, node1, node2):
		return node2 in self.neighbor_indices(node1)
