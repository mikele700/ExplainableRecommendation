from statistics import mean

from par import parse_args, set_paras, set_files, set_basic_info
import pandas as pd
import math
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import numpy as np


if __name__ == '__main__':
    args = parse_args()
    set_paras(args)
    set_files(args)
    set_basic_info(args)
    fold = 0
    names = ['user', 'item', 'predRating', 'cluster', 'i0', 'i0sim', 'i1', 'i1sim', 'i2', 'i2sim', 'u0', 'u0sim', 'u1',
             'u1sim', 'u2', 'u2sim', 'f0', 'f1', 'f2', 'f3', 'f4']
for i in range(30):
    expDF = pd.read_csv("../data/%s/prediction/pred_%d.txt" % (args.dataset,i), sep='\t', names=names,
                        index_col=False)
    # print(expDF.head(10))
    # expDF = expDF.sort_values(['user','predRating'], ascending=False)
    n =[9]
    EP=list()
    ER=list()
    ListNPre=list()
    ListNRec=list()
    avg=expDF['i0sim'].median()
    std=expDF['i0sim'].std()
    #print(avg)
    #print(std)
    #print(std)
    similarity_threshold = 0.005
    #top-n for
    for k in range(len(n)):

        for i in range(args.max_u_id):
            dfuser = expDF.loc[expDF['user'] == i].sort_values(by=['predRating'], ascending=False).head(n[k])
            dfuserER= expDF.loc[expDF['user'] == i].sort_values(by=['predRating'], ascending=False)
            size = len(dfuser.index)
            countEx=0
            countEp=0

            if(not size==0):
                #for precision
                for index, row in dfuser.iterrows():
                    #if not (math.isnan(row['i0'])) or not (math.isnan(row['u0'])) or not (math.isnan(row['f0'])):
                    if (not (math.isnan(row['i0'])) and (float(row['i0sim'])  > similarity_threshold)) or (not (math.isnan(row['u0'])) and (float(row['u0sim'])> similarity_threshold)) or not (math.isnan(row['f0'])):
                        countEx+=1
                EP.append(countEx/size)

                #for recall
                for index, row in dfuserER.iterrows():
                    #if not (math.isnan(row['i0'])) or not (math.isnan(row['u0'])) or not (math.isnan(row['f0'])):
                    if (not (math.isnan(row['i0'])) and (float(row['i0sim'])  > similarity_threshold)) or (not (math.isnan(row['u0'])) and (float(row['u0sim'])> similarity_threshold)) or not (math.isnan(row['f0'])):
                        countEp+=1
                if(not countEp==0):
                    ER.append(countEx/countEp)
                else:
                    ER.append(0)
        #print(ER[0])
        #print(ER[1])
        #print(ER[12])
        MEP = mean(EP)
        MER = mean(ER)
        print(MEP)
        print(MER)
        ListNPre.append(MEP)
        ListNRec.append(MER)
        print(mean(ListNPre))
        print(mean(ListNRec))
        with open("MEP.txt", "a") as fp:
            fp.write(str(MEP))
            fp.write("\n")
        with open("MER.txt", "a") as fr:
            fr.write(str(MER))
            fr.write("\n")




