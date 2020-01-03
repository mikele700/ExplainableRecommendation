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
- prediction.py
  : predicts ratings in test set and measure accuaracy

This software is free of charge under research purposes.
For commercial purposes, please contact the authors.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Import packages
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import pandas as pd


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Prediction
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def prediction(args, numfolds):
	# Arguments
	dim = args.dim
	maxR = args.max_r
	minR = args.min_r
	mu = args.mu

	# Lists to return
	Test_RMSEs = np.zeros(numfolds)
	Test_MAEs = np.zeros(numfolds)

	# For all folds
	for fold in range(numfolds):
		# File names
		vec_filename = args.learningpath + "vec_" + args.learningparas + "_%d.txt" % fold
		bias_filename = args.learningpath + "bias_" + args.learningparas + "_%d.txt" % fold
		ent_filename = args.learningpath + "entities_" + args.learningparas + "_%d.txt" % fold

		test_filename = args.inputpath + "b%d.csv" % fold

		# Read test set, entities' indices, vectors, and biases
		test = pd.read_csv(test_filename, sep='\t', names=['u', 'i', 'r'])
		entities = np.loadtxt(ent_filename).astype(int)
		vectors = np.loadtxt(vec_filename)
		biases = np.loadtxt(bias_filename)
		id_to_th = {j: i for i, j in enumerate(entities)}
        
		# Dr: set of the highest rated entities
		p_graph = args.graphpath + "p_graph_%s_%d.txt" % (args.graphparas, fold)
		df = pd.read_csv(p_graph, delimiter='\t', names=['e1', 'e2', 'w'])
		Dr = list()
		for i in range(args.max_i_id + 1):
		    Dr.append(list())
		for i, j, z in zip(df.e1, df.e2, df.w):
		    if z > (maxR * 2 / 3):
		        Dr[i].append(j)
        
        # Dp: set of the similar entities
		Dp_filename = args.learningpath + "Dp_" + args.learningparas + "_%d.txt" % fold
		Dp_file = open(Dp_filename,"r")
		Dp = list()
		for line in Dp_file:
			words = list(map(int,line.split()))
			Dp.append(words)
		Dp_file.close()
        
		top_items = list()
		top_item_similarities = list()
		top_users = list()
		top_user_similarities = list()
		friends = list()
		max_similarity = 0


		# Predict ratings in test set
		prediction = list()
		for u, i, r in zip(test.u, test.i, test.r):
			user = int(u)
			item = int(i)
			top_3_items = list()
			top_3_users = list()
			top_3_item_similarities = list()
			top_3_user_similarities = list()
			friends_liked = list()
			loacal_max = 0
            

			# If both user and item are not learned in train
			if not (user in entities) and not (item in entities):
				hat_r_ui = (maxR - minR) * (np.random.random()) + minR
				# hat_r_ui = round_0_5(hat_r_ui)
				prediction.append(hat_r_ui)
				continue

			# If user and item are learned in train
			if (user in entities) and (item in entities):
				# Get user vector and bias
				u_th = id_to_th[user]
				u_vec = vectors[u_th]
				b_u = biases[u_th]

				# Get item vector and bias
				i_th = id_to_th[item]
				i_vec = vectors[i_th]
				b_i = biases[i_th]
                
                # Get explaination
				top_3_items, top_3_item_similarities, friends_liked, top_3_users, top_3_user_similarities, local_max = explain(Dr, Dp, user, item, args.min_u_id, args.max_u_id)

			# If only user is learned in train
			elif (user in entities):
				# Get user vector
				u_th = id_to_th[user]
				u_vec = vectors[u_th]
				b_u = biases[u_th]

				# Get randomly initialized item vector
				a = np.sqrt((maxR + minR) / dim) / 2
				i_vec = np.random.random(dim) * a
				b_i = np.random.rand() * (a / 2)

			# If only item is learned in train
			elif (item in entities):
				# Get item vector
				i_th = id_to_th[item]
				i_vec = vectors[i_th]
				b_i = biases[i_th]

				# Get randomly initialized user vector
				a = np.sqrt((maxR + minR) / dim) / 2
				u_vec = np.random.random(dim) * a
				b_u = np.random.rand() * (a / 2)

			inn = np.matmul(u_vec, i_vec)
			hat_r_ui = mu + b_u + b_i + inn
			hat_r_ui = max(minR, min(maxR, hat_r_ui))
			prediction.append(hat_r_ui)
			top_items.append(top_3_items)
			top_item_similarities.append(top_3_item_similarities)
			top_users.append(top_3_users)
			top_user_similarities.append(top_3_user_similarities)
			friends.append(friends_liked)
			if local_max > max_similarity:
				max_similarity = local_max
			
			
		# 4. Calculate errors
		Test_MAEs[fold] = np.mean(np.abs(prediction - test.r))
		Test_RMSEs[fold] = np.sqrt(np.mean((prediction - test.r) ** 2))
        
		#threshold = max_similarity * 2 / 3
        
		# 5. Save the prediction results
		pred_filename = "../data/%s/prediction/pred_%d.txt" % (args.dataset, fold)
		with open(pred_filename, mode='w') as f:
			for u, i, p, ti, tis, tu, tus, fr in zip(test.u, test.i, prediction, top_items, top_item_similarities, top_users, top_user_similarities, friends):
				f.write("%d\t%d\t%.5f" % (u, i, p))
				for j in range(3):
					if len(ti) > j:
						#if tis[j] > threshold:
						f.write("\ti%d: %d\t%.5f" % (j, ti[j], tis[j]))
					if len(tu) > j:
						#if tus[j] > threshold:
						f.write("\tu%d: %d\t%.5f" % (j, tu[j], tus[j]))
				for j in range(len(fr)):
					f.write("\tf%d: %d" % (j, fr[j]))
				f.write("\n")
                    
		print("%s is made" %pred_filename)


	return Test_RMSEs, Test_MAEs


def explain(Dr, Dp, target_user, target_item, min_u_id, max_u_id):
    # Simple functions to determine an entity is user or item
    is_u = (lambda x: x >= min_u_id and x <= max_u_id)
    
    friends = list()
    items = list()
    similarity = list()
    top_3_items = list()
    top_3_users = list()
    top_3_item_similarities = list()
    top_3_user_similarities = list()
    users = list()
    friends_liked = list()
    max_similarity = 0
    
    # Search of the user's highest rated items. Evaluate their similarity with the target item
    e_rated = Dr[target_user]
    e_similar = Dp[target_item]
    for i in range(len(e_rated)):
        if is_u(e_rated[i]):
            friends.append(e_rated[i])
        elif e_similar.count(e_rated[i]) > 0:
            items.append(e_rated[i])
            similarity.append(2 * e_similar.count(e_rated[i]) / (len(e_similar) + len(Dp[e_rated[i]])))
            
    if len(items) > 0:
        max_similarity = max(similarity)
        max_S = max_similarity
        for i in range(3):
            max_index = similarity.index(max_S)
            top_3_items.append(items[max_index])
            top_3_item_similarities.append(max_S)
            items.pop(max_index)
            similarity.pop(max_index)
            if len(items) == 0:
                break
            max_S = max(similarity)
    
    # Searching of users who liked the target item. Evaluate their similarity with the target user        
    e_rated = Dr[target_item]
    e_similar = Dp[target_user]
    similarity = list()
    for i in range(len(e_rated)):
        if e_rated[i] in friends:
            friends_liked.append(e_rated[i])
        elif e_similar.count(e_rated[i]) > 0:
            users.append(e_rated[i])
            similarity.append(2 * e_similar.count(e_rated[i]) / (len(e_similar) + len(Dp[e_rated[i]])))
    
    if len(users) > 0:     
        max_S = max(similarity)
        if max_S > max_similarity:
            max_similarity = max_S
        for i in range(3):
            max_index = similarity.index(max_S)
            top_3_users.append(users[max_index])
            top_3_user_similarities.append(max_S)
            users.pop(max_index)
            similarity.pop(max_index)
            if len(users) == 0:
                break
            max_S = max(similarity)
    
    
    return top_3_items, top_3_item_similarities, friends_liked, top_3_users, top_3_user_similarities, max_similarity


