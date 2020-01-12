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
- main.py
  : runs Uniwalk algorithm

This software is free of charge under research purposes.
For commercial purposes, please contact the authors.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Import packages
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import sys
from time import localtime
from par import parse_args, set_paras, set_files, set_basic_info, print_args
from embedding import embedding
from prediction import prediction
from build_graph import build_graph
#from split_5_folds import split_5_folds
from xval import xval
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Additional functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Print the present time
def now_string():
	now = localtime()
	now_day = (now.tm_year, now.tm_mon, now.tm_mday)
	now_time = (now.tm_hour, now.tm_min)
	s = "%04d-%02d-%02d_" % now_day + "%02d-%02d" % now_time
	return s



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Main method
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
	# 1. Get arguments
	args = parse_args()
	set_paras(args)
	set_files(args)
	set_basic_info(args)
	print_args(args)
    

	# 2. Split input ratings into 5 folds
	#split_5_folds(args.dataset, 5)
	#xval(args.dataset, 5)

	# 3. Build graph
	#build_graph(args, 5)

	# 4. Learn
	numfold = 1
	sampling_type = ['positive', 'negative', 'unweighted']
	Train_RMSEs = list()
	min_TestRMSEs = list()
	min_TestMAEs = list()
	
	#for fold in range(numfold):
	#	rmse, min_TestRMSE, min_TestMAE = embedding(args, fold, sampling_type)
	#	prtstr = "Fold = %d, rmse = %.3f" % (fold, rmse)
	#	print(prtstr)
	#	prtstr = "Fold = %d, min rmse = %.3f" % (fold, min_TestRMSE)
	#	print(prtstr)
	#	prtstr = "Fold = %d, min mae = %.3f" % (fold, min_TestMAE)
	#	print(prtstr)
	#	Train_RMSEs.append(rmse)
	#	min_TestRMSEs.append(min_TestRMSE)
	#	min_TestMAEs.append(min_TestMAE)
	
	#prtstr = "Train RMSEs = %s" % Train_RMSEs
	#print(prtstr)
	
	# 5. Prediction
	Test_RMSEs, Test_MAEs = prediction(args, numfold)

	
