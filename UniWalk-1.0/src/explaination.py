
from par import parse_args, set_paras, set_files, set_basic_info
import random
import math
import pandas as pd

def explanation(df, randUser):
    for index, row in df.iterrows():
        s = "Logged User: " + str(randUser) + "\nWe recommend you item: " + str(int(row['item']))
        if not math.isnan(row['i0']):
            s += "\nYou like other similiar items: " + str(int(row['i0'])) + " "
        if not math.isnan(row['i1']):
            s += str(int(row['i1'])) + " "
        if not math.isnan(row['i2']):
            s += str(int(row['i2']))
        
        if not math.isnan(row['u0']):
            exp_u = "\nMoreover, the following users, who are similiar to you, preferred that item: "
            s += exp_u + str(int(row['u0'])) + " "
        if not math.isnan(row['u1']):
            s += str(int(row['u1'])) + " "
        if not math.isnan(row['u2']):
            s += str(int(row['u2']))
        
        if not math.isnan(row['f0']):
            exp_f = "\nAdditionaly, the following friends of yours preferred that item: "
            s += exp_f + str(int(row['f0'])) + " "
        if not math.isnan(row['f1']):
            s += str(int(row['f1'])) + " "
        if not math.isnan(row['f2']):
            s += str(int(row['f2']))
        if not math.isnan(row['f3']):
            s += str(int(row['f3'])) + " "
        if not math.isnan(row['f4']):
            s += str(int(row['f4']))
            
        s += "\n"
        print(s)

def persexplanation(df, randUser, profile):
    for index, row in df.iterrows():
        s = "Logged User: " + str(randUser) + "\t Personality: " + str(profile[randUser]) + "\nWe recommend you item: " + str(int(row['item'])) + "\nUsers with personality similar to yours preferred that item"
        if not math.isnan(row['i0']):
            s += "\nFurthermore, you like other similiar items: " + str(int(row['i0'])) + " "
        if not math.isnan(row['i1']):
            s += str(int(row['i1'])) + " "
        if not math.isnan(row['i2']):
            s += str(int(row['i2']))
        
        if not math.isnan(row['u0']):
            exp_u = "\nMoreover, the following users, who are similiar to you, preferred that item: "
            s += exp_u + str(int(row['u0'])) + " "
            if profile[randUser] == profile[int(row['u0'])]:
                s += "(personality similarity) "
        if not math.isnan(row['u1']):
            s += str(int(row['u1'])) + " "
            if profile[randUser] == profile[int(row['u1'])]:
                s += "(personality similarity) "
        if not math.isnan(row['u2']):
            s += str(int(row['u2']))
            if profile[randUser] == profile[int(row['u2'])]:
                s += "(personality similarity) "
        
        if not math.isnan(row['f0']):
            exp_f = "\nAdditionaly, the following friends of yours preferred that item: "
            s += exp_f + str(int(row['f0'])) + " "
        if not math.isnan(row['f1']):
            s += str(int(row['f1'])) + " "
        if not math.isnan(row['f2']):
            s += str(int(row['f2']))
        if not math.isnan(row['f3']):
            s += str(int(row['f3'])) + " "
        if not math.isnan(row['f4']):
            s += str(int(row['f4']))
            
        s += "\n"
        print(s)
        
def combinedexplanation(df, randUser, profile):
    for index, row in df.iterrows():
        s = "Logged User: " + str(randUser) + "\t Personality: " + str(profile[randUser]) + "\nWe recommend you item: " + str(int(row['item']))
        if profile[randUser] == int(row['cluster']):
             s += "\nUsers with personality similar to yours preferred that item"
        if not math.isnan(row['i0']):
            s += "\nFurthermore, you like other similiar items: " + str(int(row['i0'])) + " "
        if not math.isnan(row['i1']):
            s += str(int(row['i1'])) + " "
        if not math.isnan(row['i2']):
            s += str(int(row['i2']))
        
        if not math.isnan(row['u0']):
            exp_u = "\nMoreover, the following users, who are similiar to you, preferred that item: "
            s += exp_u + str(int(row['u0'])) + " "
            if profile[randUser] == profile[int(row['u0'])]:
                s += "(personality similarity) "
        if not math.isnan(row['u1']):
            s += str(int(row['u1'])) + " "
            if profile[randUser] == profile[int(row['u1'])]:
                s += "(personality similarity) "
        if not math.isnan(row['u2']):
            s += str(int(row['u2']))
            if profile[randUser] == profile[int(row['u2'])]:
                s += "(personality similarity) "
        
        if not math.isnan(row['f0']):
            exp_f = "\nAdditionaly, the following friends of yours preferred that item: "
            s += exp_f + str(int(row['f0'])) + " "
        if not math.isnan(row['f1']):
            s += str(int(row['f1'])) + " "
        if not math.isnan(row['f2']):
            s += str(int(row['f2']))
        if not math.isnan(row['f3']):
            s += str(int(row['f3'])) + " "
        if not math.isnan(row['f4']):
            s += str(int(row['f4']))
            
        s += "\n"
        print(s)


if __name__ == '__main__':
    
    args = parse_args()
    set_paras(args)
    set_files(args)
    set_basic_info(args)
    fold = 0
    mode = 2
    
    names = ['user', 'item', 'predRating', 'cluster', 'i0', 'i0sim', 'i1', 'i1sim', 'i2', 'i2sim', 'u0', 'u0sim', 'u1', 'u1sim', 'u2', 'u2sim', 'f0', 'f1', 'f2', 'f3', 'f4']
    expDF = pd.read_csv("../data/%s/prediction/pred_%d.txt" %(args.dataset, fold), sep='\t', names=names, index_col=False)
    randUser = random.randrange(args.min_u_id, args.max_u_id + 1)
    
    if mode == 0:
        expDF = expDF.loc[expDF['user'] == randUser].sort_values(by=['predRating'], ascending=False).head(3)
        if expDF.empty:
            print("No recommendation available for target user " + str(randUser))
        else:
            explanation(expDF, randUser)
    elif mode == 1:
        profile = list()
        profile_filename = args.inputpath + "random_profile.txt"
        with open(profile_filename, mode='r') as f:
            for line in f:
                profile.append(int(line))
        expDF = expDF.loc[(expDF['user'] == randUser) & (expDF['cluster'] == profile[randUser])].sort_values(by=['predRating'], ascending=False).head(3)
        if expDF.empty:
            print("No recommendation available for target user " + str(randUser))
        else:
            persexplanation(expDF, randUser, profile)
    elif mode == 2:
        profile = list()
        profile_filename = args.inputpath + "random_profile.txt"
        with open(profile_filename, mode='r') as f:
            for line in f:
                profile.append(int(line))
        expDF = expDF.loc[expDF['user'] == randUser].sort_values(by=['predRating'], ascending=False).head(5)
        order = []
        for i in range(len(expDF.index)):
            order.append(i)
        i = 0
        for index, row in expDF.iterrows():
            if profile[randUser] == int(row['cluster']):
                order[i] -= 2
            i += 1
        expDF['order'] = order
        expDF = expDF.sort_values(by=['order'], ascending=True).head(3)
                
        if expDF.empty:
            print("No recommendation available for target user " + str(randUser))
        else:
            combinedexplanation(expDF, randUser, profile)



