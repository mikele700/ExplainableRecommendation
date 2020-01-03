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
from walk import *
from helper import *


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Network embedding
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def embedding(args, fold, sampling_types):
	# Read graph
	p_graph = args.graphpath + "p_graph_%s_%d.txt" % (args.graphparas, fold)
	n_graph = args.graphpath + "n_graph_%s_%d.txt" % (args.graphparas, fold)
	p_g = read_graph(p_graph)
	r_g = read_graph(n_graph)

	# Read ratings
	train = read_train_ratings(args, fold)
	test = read_test_ratings(args, fold)

	# Initialize vectors and biases of entities
	args.num_entities = p_g.number_of_nodes()
	B, Z, Dp = init_learn(args)

	# Make transition tables
	id_to_th, transition_dict = make_transit(args, p_g)
	_, r_transition_dict = make_transit(args, r_g)
	
	# Initialize velocity tables
	bias_v, vec_s_v, vec_up_v, vec_un_v = dict(), dict(), dict(), dict()
	
	# Initialize learning variables
	prev_set_rmse, set_iter, min_TestRMSE, min_TestMAE = 10, 0, 10, 10

	# Learn a set of walks
	while set_iter < args.max_sets:
		print("=" * 21 + " %d-th set " % set_iter + "=" * 21)

		# Get walks
		un_walks = do_walk(args, p_g, dict(), 'unweighted')
		po_walks = do_walk(args, p_g, transition_dict, 'positive')
		ne_walks = do_walk(args, r_g, transition_dict, 'negative')
		
		# Initialize inner learning variables
		circuit_iter, prev_circuit_rmse, prev_test_rmse = 0, 10, 10
		
		# Inner learning
		while circuit_iter < args.max_circuits:
			print("-" * 19 + " %d-th circuit " % circuit_iter + "-" * 19)

			for sampling_type in sampling_types:
				# Learn from the each walk
				if sampling_type == 'unweighted':
					unweighted_circuit_rmse, bias_v, vec_s_v, vec_up_v, vec_un_v = learning_1_unit(args, fold, id_to_th, p_g, un_walks, Z, B, Dp, sampling_type, train, bias_v, vec_s_v, vec_up_v, vec_un_v)
					circuit_rmse = unweighted_circuit_rmse
				elif sampling_type == 'positive':
					positive_circuit_rmse, bias_v, vec_s_v, vec_up_v, vec_un_v = learning_1_unit(args, fold, id_to_th, p_g, po_walks, Z, B, Dp, sampling_type, train, bias_v, vec_s_v, vec_up_v, vec_un_v)
					circuit_rmse = positive_circuit_rmse
				elif sampling_type == 'negative':
					positive_circuit_rmse, bias_v, vec_s_v, vec_up_v, vec_un_v = learning_1_unit(args, fold, id_to_th, r_g, ne_walks, Z, B, Dp, sampling_type, train, bias_v, vec_s_v, vec_up_v, vec_un_v)
					circuit_rmse = positive_circuit_rmse
				else:
					print('Err, invalid type of sampling')
				print('train rmse from %s walk: %.3f\n' % (sampling_type, circuit_rmse))

				# Check whether the circuit learning converges
				is_conv = (np.abs(prev_circuit_rmse - circuit_rmse) < args.conv)
				if is_conv:
					print('is_conv', prev_circuit_rmse, circuit_rmse)
					circuit_iter = args.max_circuits
					break
				prev_circuit_rmse = circuit_rmse
				
				if not (circuit_iter == 0) and (prev_circuit_rmse < circuit_rmse):
					print("Go to the next set, even though it does not converge.")
					print("RMSE is increased, from %.3f to %.3f." % (prev_circuit_rmse, circuit_rmse))
					circuit_iter = args.max_circuits
					break

			# Ready to the next circuit
			circuit_iter += 1
			prev_circuit_rmse = circuit_rmse
			
			print("-" * 19 + " %d-th circuit " % (circuit_iter - 1) + "-" * 19)
			

			# Check test rmse and test mae
			prediction = list()
			nodes = p_g.nodes()
			for u, i in zip(test.u, test.i):
				user = int(u)
				item = int(i)
				# If both user and item are not learned in train
				if not (user in nodes) and not (item in nodes):
					hat_r_ui = (args.max_r - args.min_r) * (np.random.random()) + args.min_r
					prediction.append(hat_r_ui)
					continue

				# If user and item are learned in train
				if (user in nodes) and (item in nodes):
					# Get user vector and bias
					u_th = id_to_th[user]
					u_vec = Z[u_th]
					b_u = B[u_th]

					# Get item vector and bias
					i_th = id_to_th[item]
					i_vec = Z[i_th]
					b_i = B[i_th]


				# If only user is learned in train
				elif (user in nodes):
					# Get user vector
					u_th = id_to_th[user]
					u_vec = Z[u_th]
					b_u = B[u_th]

					# Get randomly initialized item vector
					a = np.sqrt((args.max_r + args.min_r) / args.dim) / 2
					i_vec = np.random.random(args.dim) * a
					b_i = np.random.rand() * (a / 2)

				# If only item is learned in train
				elif (item in nodes):
					# Get item vector
					i_th = id_to_th[item]
					i_vec = Z[i_th]
					b_i = B[i_th]

					# Get randomly initialized user vector
					a = np.sqrt((args.max_r + args.min_r) / args.dim) / 2
					u_vec = np.random.random(args.dim) * a
					b_u = np.random.rand() * (a / 2)

				inn = np.matmul(u_vec, i_vec)
				hat_r_ui = args.mu + b_u + b_i + inn
				hat_r_ui = max(args.min_r, min(args.max_r, hat_r_ui))
				prediction.append(hat_r_ui)
			TestRMSE = np.sqrt(np.mean(np.subtract(prediction, test.r) ** 2))
			TestMAE = np.mean(np.absolute(np.subtract(prediction, test.r)))
			min_TestRMSE = min(min_TestRMSE, TestRMSE)
			min_TestMAE = min(min_TestMAE, TestMAE)
			
			print('TestRMSE: ', TestRMSE)
			
			if prev_test_rmse < TestRMSE:
				print('test rmse increase, so break')
				break
			prev_test_rmse = TestRMSE			

		# Check whether the set learning converges
		set_rmse = circuit_rmse
		if (np.abs(prev_set_rmse - set_rmse) < args.conv):
			break
		if not (set_iter == 0) and (prev_set_rmse < set_rmse):
			print("Go to the next set, even though it does not converge.")
			print("RMSE is increased, from %.3f to %.3f." % (prev_set_rmse, prev_set_rmse))
			break
		print('train rmse from %d set: %.3f\n' % (set_iter, circuit_rmse))

		# Ready to the next set
		set_iter += 1
		prev_set_rmse = set_rmse
		print("=" * 21 + " %d-th set " % set_iter + "=" * 21)

	rmse = set_rmse

	# 8. Save the learning results
	Dp_filename = args.learningpath + "Dp_" + args.learningparas + "_%d.txt" % fold    
	vec_filename = args.learningpath + "vec_" + args.learningparas + "_%d.txt" % fold
	bias_filename = args.learningpath + "bias_" + args.learningparas + "_%d.txt" % fold
	ent_filename = args.learningpath + "entities_" + args.learningparas + "_%d.txt" % fold
	np.savetxt(vec_filename, Z, fmt='%.5f', delimiter='\t')
	np.savetxt(bias_filename, B, fmt='%.5f', delimiter='\t')
	np.savetxt(ent_filename, nodes, fmt='%d', delimiter='\t')
	with open(Dp_filename, mode='w') as f:
		for i in range(len(Dp)):
			for j in range(len(Dp[i])):
				f.write("%d\t" %Dp[i][j] )
			f.write("\n")

	return rmse, min_TestRMSE, min_TestMAE


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Embedding a single set of walks
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def learning_1_unit(args, fold, node_to_th, g, walks, Z, B, Dp, sampling, train, bias_v, vec_s_v, vec_up_v, vec_un_v):
	# Get parameters
	a = args.alpha
	b = args.beta
	m = args.gamma
	mu = args.mu
	lz = args.lz
	lb = args.lb
	lr = args.lr
	ws = args.ws
	dim = args.dim
	minR = args.min_r
	maxR = args.max_r
	min_u_id = args.min_u_id
	max_u_id = args.max_u_id
	min_i_id = args.min_i_id
	max_i_id = args.max_i_id

	# Simple functions to determine an entity is user or item
	is_u = (lambda x: x >= min_u_id and x <= max_u_id)
	is_i = (lambda x: x >= min_i_id and x <= max_i_id)

	# Learning
	# For all walks and weights in a single set
	for walk in walks:
		# Get a walk of nodes
		num_case_of_slides = len(walk) - ws + 1
		if num_case_of_slides < 1:
			continue

		# For all slides in walk w
		for ith_slide in range(num_case_of_slides):
			# Get target node that is in the center of the window
			target_pos = ith_slide + int(ws / 2)
			trg = walk[target_pos]

			# Learn entities' vectors in the window
			for ith_pos in range(ith_slide, ith_slide + ws):
				# Get a negighbor node
				nei = walk[ith_pos]
				if nei == trg:
					continue

				# Ready to update vector and bias of target node and i-th neighbor node
				vec_target = Z[node_to_th[trg]]
				vec_ith = Z[node_to_th[nei]]
				b_target = B[node_to_th[trg]]
				b_ith = B[node_to_th[nei]]

				# Get the type of the pair
				is_connected = g.connected(nei, trg)
				is_ui_pair = (is_u(nei) and is_i(trg)) or (is_u(trg) and is_i(nei))
			
				# Supervised update when the two nodes are connected
				if is_connected and is_ui_pair:
					# Get error
					rz = g.weight_bw_nodes(nei, trg)
					err = rz - (mu + b_target + b_ith + np.matmul(vec_ith, vec_target))

					# Set up velocity tables
					if not ((trg, nei) in bias_v):
						bias_v[(trg, nei)] = 0
						bias_v[(nei, trg)] = 0
						vec_s_v[(trg, nei)] = np.zeros(dim)
						vec_s_v[(nei, trg)] = np.zeros(dim)
					vec_s_v[(trg, nei)] = lr * (- err * vec_ith + lz * vec_target) + m * vec_s_v[(trg, nei)]
					vec_s_v[(nei, trg)] = lr * (- err * vec_target + lz * vec_ith) + m * vec_s_v[(nei, trg)]
					bias_v[(trg, nei)] = lr * (- err + lb * b_target) + m * bias_v[(trg, nei)]
					bias_v[(nei, trg)] = lr * (- err + lb * b_ith) + m * bias_v[(nei, trg)]

					# Update vectors and biases, optimizing the supervised term
					Z[node_to_th[trg]] -= vec_s_v[(trg, nei)]
					Z[node_to_th[nei]] -= vec_s_v[(nei, trg)]
					B[node_to_th[trg]] -= bias_v[(trg, nei)]
					B[node_to_th[nei]] -= bias_v[(nei, trg)]

				# Do nothing when the nodes are randomly sampled without any sense
				elif sampling == 'unweighted':
					continue

				# Unsupervised update for positive walk
				elif sampling == 'positive':
					# Update D+                   
					Dp[trg].append(nei)
					Dp[nei].append(trg)       
					# Set up velocity table
					if not ((trg, nei) in vec_up_v):
						vec_up_v[(trg, nei)] = np.zeros(dim)
						vec_up_v[(nei, trg)] = np.zeros(dim)
					vec_up_v[(trg, nei)] = a * lr * (- vec_ith + lz * vec_target) + m * vec_up_v[(trg, nei)]
					vec_up_v[(nei, trg)] = a * lr * (- vec_target + lz * vec_ith) + m * vec_up_v[(nei, trg)]

					# Update vectors, optimizing the unsupervised positive term
					Z[node_to_th[trg]] -= vec_up_v[(trg, nei)]
					Z[node_to_th[nei]] -= vec_up_v[(nei, trg)]

				# Unsupervised update for negative walk
				elif sampling == 'negative':
					if is_ui_pair:
						# Set up velocity table
						if not ((trg, nei) in vec_un_v):
							vec_un_v[(trg, nei)] = np.zeros(dim)
							vec_un_v[(nei, trg)] = np.zeros(dim)
						vec_un_v[(trg, nei)] = b * lr * (vec_ith + lz * vec_target) + m * vec_un_v[(trg, nei)]
						vec_un_v[(nei, trg)] = b * lr * (vec_target + lz * vec_ith) + m * vec_un_v[(nei, trg)]

						# Update vectors, optimizing the unsupervised positive term
						Z[node_to_th[trg]] -= vec_un_v[(trg, nei)]
						Z[node_to_th[nei]] -= vec_un_v[(nei, trg)]
					else:
						# Update D+
						Dp[trg].append(nei)
						Dp[nei].append(trg) 
						# Set up velocity table
						if not ((trg, nei) in vec_up_v):
							vec_up_v[(trg, nei)] = np.zeros(dim)
							vec_up_v[(nei, trg)] = np.zeros(dim)
						vec_up_v[(trg, nei)] = a * lr * (- vec_ith + lz * vec_target) + m * vec_up_v[(trg, nei)]
						vec_up_v[(nei, trg)] = a * lr * (- vec_target + lz * vec_ith) + m * vec_up_v[(nei, trg)]

						# Update vectors, optimizing the unsupervised positive term
						Z[node_to_th[trg]] -= vec_up_v[(trg, nei)]
						Z[node_to_th[nei]] -= vec_up_v[(nei, trg)]
						
	# Predict weights of edges
	pre_r = 0
	diff_arr = np.zeros(len(train.r))
	for u, i, r in zip(train.u, train.i, train.r):
		u = int(u)
		i = int(i)
		vec_u = Z[node_to_th[u]]
		vec_i = Z[node_to_th[i]]
		b_u = B[node_to_th[u]]
		b_i = B[node_to_th[i]]
		pred = mu + b_u + b_i + np.matmul(vec_u, vec_i)
		pred = max(min(pred, maxR), minR)
		diff_arr[pre_r] = r - pred
		pre_r += 1
		

	# Check whether this learning_1_set converges
	rmse = np.sqrt(np.mean(diff_arr ** 2))
		
	return rmse, bias_v, vec_s_v, vec_up_v, vec_un_v

