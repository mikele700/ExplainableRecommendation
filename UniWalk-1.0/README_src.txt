=====================================================
Readme of UniWalk codes (v1.0)
=====================================================


=====================================================
Contents
=====================================================
1. Basic information
2. Overview
3. Requirements
4. How to install
5. How to use
	1) Input and output
	2) How to run
	3) How to give parameters
6. Demo example


=====================================================
1. Basic information
=====================================================
- Authors: Haekyu Park, Hyunsik Jeon, Junghwan Kim, 
			Beunguk Ahn, and U Kang
- Program name: UniWalk
- Version: 1.0
- Last updated: 18 Oct 2017
- Main contact: Haekyu Park (hkpark627@snu.ac.kr)


=====================================================
2. Overview
=====================================================
This package is a set of implementaions of UniWalk: Explainable and Accurate recommendation for Rating and Network Data.


=====================================================
3. Requirements
=====================================================
- python 3.*
- numpy
- pandas
- scipy
We recommend you to use Anaconda (https://www.continuum.io/downloads).

=====================================================
4. How to install
=====================================================
You can download this code package at the project hompage. 
(https://datalab.snu.ac.kr/uniwalk)


=====================================================
5. How to use
=====================================================
1) Input and output
	- Input
		: Ratings and social network are able to be given as input.
		: All the input should be given as tab-separated files.
		:	- Rating file should have three columns for user_id, item_id, and rating.
		:	- User_id should not overlapped with item_id.
		:	- Social network file should have two columns for users.
		: The name of rating files should be 'rating.tsv'.
		: The name of social network files should be 'link.tsv'.
	- Output
		: We print out test RMSE and MAE.
	- Intermediate outputs
		: We generate intermediate outputs such as vectors and biases of users and items.
		: All the intermediate outputs are saved in './data/<dataset name>/'.

2) How to run
First go to './code/'.
You can run the code by typing 'python main.py'.
You can optionally give parameters as by appending '--argument_type argument_value'.
	For example, if you want to run matrix factorization with explicit ratings, and you want to set learning rate = 0.05, lambda = 0.3, and dimension = 5, 
	you can run the code as follows:
	python main.py --lr 0.05 --dim 5


The parameters you can give are as follows. 

	argument_type	|	default argument_value		|	details
	--------------------------------------------------------------------------
	--dataset 		| filmtrust						| Name of dataset
	--inputpath		| '../data/<dataset>/input/'	| Where datasets are
	--graphpath		| '../data/<dataset>/graph/'	| Where unified graphs are
	--learningpath	| '../data/<dataset>/learning/'	| Where results are
	--c				| 5								| Weight of user-user edges 
	--wl			| 50							| Length of walks
	--ws			| 7								| Window size 
	--alpha			| 0.05							| Weight of positive term
	--beta			| 0.005							| Weight of negative term
	--gamma			| 0.2							| Momentum parameter
	--dim 			| 25							| Dimension of vectors
	--lr 			| 0.05							| Learning rate
	--lz 			| 0.1							| Regularization for vector
	--lb 			| 0.1							| Regularization for bias
	


=====================================================
6. Demo example
=====================================================
You can run UniWalk with filmtrust dataset.
Please run demo.sh by typing './demo.sh'.

