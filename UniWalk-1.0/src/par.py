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
- parser.py
  : controls hyperparameters

This software is free of charge under research purposes.
For commercial purposes, please contact the authors.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Import Package
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import argparse
import numpy as np
import pandas as pd



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Parse arguments
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Define hyperparameters
def parse_args():
	# Create an argument parser
	parser = argparse.ArgumentParser('UniWalk')

	# Arguments related to input
	parser.add_argument('--dataset', default='filmtrust', help='Dataset name')
	parser.add_argument('--min_u_id', default=0, help='Min id of users')
	parser.add_argument('--max_u_id', default=1641, help='Max id of users')
	parser.add_argument('--min_i_id', default=1642, help='Min id of items')
	parser.add_argument('--max_i_id', default=3712, help='Max id of items')
	parser.add_argument('--max_r', default=0.5, help='Max of observed rating')
	parser.add_argument('--min_r', default=4.0, help='Min of observed rating')
	parser.add_argument('--mu', default=3, help='Average observed rating')
	parser.add_argument('--num_entities', default=0, help='Number of entities')

	# Arguments related to file paths
	parser.add_argument('--inputpath', default='', help='Path of data files')
	parser.add_argument('--graphpath', default='', help='Path of unified graph')
	parser.add_argument('--learningpath', default='', help='Path of result files')
	
	# Arguments related to building graph
	parser.add_argument('--c', default=5, help='Weight of user-user edges')

	# Arguments related to the sampling phase
	parser.add_argument('--wl', default=50, help='Walk length')

	# Arguments related to the optimization phase
	parser.add_argument('--ws', default=7, help='Window size')
	parser.add_argument('--alpha', default=0.01, help='Weight of positive term')
	parser.add_argument('--beta', default=0.005, help='Weight of negative term')
	parser.add_argument('--gamma', default=0.2, help='Momentum parameter')
	parser.add_argument('--dim', default=25, help='Dimension of embedded vectors')
	parser.add_argument('--lz', default=0.1, help='Regularization parameter for vector')
	parser.add_argument('--lb', default=0.1, help='Regularization parameter for bias')
	parser.add_argument('--lr', default=0.01, help='Learning rate')
	parser.add_argument('--max_circuits', default=7, help='Maximal number of circuits to learn')
	parser.add_argument('--max_sets', default=4, help='Maximal number of sets to learn')
	parser.add_argument('--conv', default=0.0001, help='Convergence threshold')

	# Arguments related to file names to be saved
	parser.add_argument('--graphparas', default='', help='Parameters for building graph')
	parser.add_argument('--learningparas', default='', help='Parameters for learning')

	return parser.parse_args()


# Set parameters of string to numbers
def set_paras(args):
	args.min_u_id = int(args.min_u_id)
	args.max_u_id = int(args.max_u_id)
	args.min_i_id = int(args.min_i_id)
	args.max_i_id = int(args.max_i_id)
	args.mu = float(args.mu)
	args.max_r = float(args.max_r)
	args.min_r = float(args.min_r)
	args.c = float(args.c)
	args.ws = int(args.ws)
	args.wl = int(args.wl)
	args.alpha = float(args.alpha)
	args.beta = float(args.beta)
	args.dim = int(args.dim)
	args.lb = float(args.lb)
	args.lz = float(args.lz)
	args.gamma = float(args.gamma)
	args.max_sets = int(args.max_sets)
	args.max_circuits = int(args.max_circuits)


# Define file paths and names
def set_files(args):
	dataset = args.dataset
	args.inputpath = '../data/%s/input/' % dataset
	args.graphpath = '../data/%s/graph/' % dataset
	args.learningpath = '../data/%s/learning/' % dataset
	args.graphparas = '%s' % args.c
	args.learningparas = '%s_%s_%s_%s_%s_%s_%s_%s_%s' % \
		(args.alpha, args.beta, args.gamma, args.dim, args.lb, args.lz, args.lr, args.ws, args.wl)


# Set basic info of ratings
def set_basic_info(args):
	# Read rating
	rui = pd.read_csv(args.inputpath + 'rating.tsv', sep='\t', names=['u', 'i', 'r'])

	# Set min and max of ids
	args.min_u_id = min(rui.u)
	args.max_u_id = max(rui.u)
	args.min_i_id = min(rui.i)
	args.max_i_id = max(rui.i)

	# Set max and min of rating
	args.max_r = max(rui.r)
	args.min_r = min(rui.r)

	# Set mu
	args.mu = np.average(rui.r)


# Print the setted arguments
def args_to_string(args):
	s = "-------------------- Arguments ---------------------\n"
	s += "dataset = %s\n" % args.dataset
	s += "c = %s\n" % args.c
	s += "wl = %s\n" % args.wl
	s += "ws = %s\n" % args.ws
	s += "lr = %s\n" % args.lr
	s += "dim = %s\n" % args.dim
	s += "alpha = %s\n" % args.alpha
	s += "beta = %s\n" % args.beta
	s += "gamma = %s\n" % args.gamma
	s += "lambda_z = %s\n" % args.lz
	s += "lambda_b = %s\n" % args.lb
	s += "-------------------- Arguments ---------------------\n"
	return s


# Print the arguments
def print_args(args):
	print(args_to_string(args))


