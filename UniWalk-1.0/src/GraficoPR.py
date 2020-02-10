from statistics import mean

from par import parse_args, set_paras, set_files, set_basic_info
import pandas as pd
import math
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2

if __name__ == '__main__':
    args = parse_args()
    set_paras(args)
    set_files(args)
    set_basic_info(args)
    fold = 2
    names = ['user', 'item', 'predRating', 'cluster', 'i0', 'i0sim', 'i1', 'i1sim', 'i2', 'i2sim', 'u0', 'u0sim', 'u1',
             'u1sim', 'u2', 'u2sim', 'f0', 'f1', 'f2', 'f3', 'f4']
    expDF = pd.read_csv("../data/%s/prediction/pred_%d.txt" % (args.dataset,fold), sep='\t', names=names,
                        index_col=False)

    ListNPre = list()
    ListNRec = list()
    similarity_threshold = 0.005
    n =[3,4,5,6,7,8,9]
    for k in range(3,10):
        EP = list()
        ER = list()
        print(k)
        for i in range(args.max_u_id):
            dfuser = expDF.loc[expDF['user'] == i].sort_values(by=['predRating'], ascending=False).head(k)
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
        MEP = mean(EP)
        MER = mean(ER)
        print(MEP,MER)
        ListNPre.append(MEP)
        ListNRec.append(MER)

plt1.plot(n, ListNPre, label='Precision',color='r',marker='o')
plt1.title("Precision soglia %0.4f" % similarity_threshold)
plt1.ylim(min(ListNPre) - 0.01, max(ListNPre) + 0.01)
# plt.yticks(np.arange(0.8, 0.9, 0.01))
plt1.legend()
plt1.show()
plt2.plot(n, ListNRec, label='Recall',color='r',marker='o')
plt2.title("Recall soglia %0.4f" % similarity_threshold)
plt2.legend()
plt2.show()
#plt1.savefig('Precision FilmTrust')
#plt2.savefig('Recall FilmTrust')