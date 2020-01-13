
from par import parse_args, set_paras, set_files, set_basic_info
import random
import math
import pandas as pd

def explanation(df, randUser, args):
    if args.dataset == "steam":
        users, items = detail(args)
        user = users[randUser]
    else:
        user = str(randUser)
    for index, row in df.iterrows():
        s = "Logged User: " + user + "\nWe recommend you: "
        if args.dataset == "steam":
            s += detailitem(int(row['item']), items, args)
        else:
            s += "item " + str(int(row['item']))
        
        if not math.isnan(row['i0']):
            s += "\nYou like other similiar items:\n- "
            if args.dataset == "steam":
                s += detailitem(int(row['i0']), items, args)
            else:
                s += "Item " + str(int(row['i0']))
        if not math.isnan(row['i1']):
            s += "\n- "
            if args.dataset == "steam":
                s += detailitem(int(row['i1']), items, args)
            else:
                s += "Item " + str(int(row['i1']))
        if not math.isnan(row['i2']):
            s += "\n- "
            if args.dataset == "steam":
                s += detailitem(int(row['i2']), items, args)
            else:
                s += "Item " + str(int(row['i2']))
        
        if not math.isnan(row['u0']):
            exp_u = "\nMoreover, the following users, who are similiar to you, preferred that item:\n"
            if args.dataset == "steam":
                u0 = users[int(row['u0'])]
            else:
                u0 = str(int(row['u0']))
            s += exp_u + "- User: " + u0
        if not math.isnan(row['u1']):
            if args.dataset == "steam":
                u1 = users[int(row['u1'])]
            else:
                u1 = str(int(row['u1']))
            s += "\n- User: " + u1
        if not math.isnan(row['u2']):
            if args.dataset == "steam":
                u2 = users[int(row['u2'])]
            else:
                u2 = str(int(row['u2']))
            s += "\n- User: " + u2
        
        if not math.isnan(row['f0']):
            exp_f = "\nAdditionaly, the following friends of yours preferred that item:\n"
            if args.dataset == "steam":
                f0 = users[int(row['f0'])]
            else:
                f0 = str(int(row['f0']))
            s += exp_f + "- Friend: " + f0
        if not math.isnan(row['f1']):
            if args.dataset == "steam":
                f1 = users[int(row['f1'])]
            else:
                f1 = str(int(row['f1']))
            s += "\n- Friend: " + f1
        if not math.isnan(row['f2']):
            if args.dataset == "steam":
                f2 = users[int(row['f2'])]
            else:
                f2 = str(int(row['f2']))
            s += "\n- Friend: " + f2
        if not math.isnan(row['f3']):
            if args.dataset == "steam":
                f3 = users[int(row['f3'])]
            else:
                f3 = str(int(row['f3']))
            s += "\n- Friend: " + f3
        if not math.isnan(row['f4']):
            if args.dataset == "steam":
                f4 = users[int(row['f4'])]
            else:
                f4 = str(int(row['f4']))
            s += "\n- Friend: " + f4
            
        s += "\n"
        print(s)

def persexplanation(df, randUser, profile):
    if args.dataset == "steam":
        users, items = detail(args)
        user = users[randUser]
    else:
        user = str(randUser)
    for index, row in df.iterrows():
        s = "Logged User: " + user + "\nPersonality: " + str(profile[randUser]) + "\nWe recommend you: "
        if args.dataset == "steam":
            s += detailitem(int(row['item']), items, args)
        else:
            s += "item " + str(int(row['item']))
            
        if profile[randUser] == int(row['cluster']):
             s += "\nUsers with personality similar to yours preferred that item"
        
        if not math.isnan(row['i0']):
            s += "\nYou like other similiar items:\n- "
            if args.dataset == "steam":
                s += detailitem(int(row['i0']), items, args)
            else:
                s += "Item " + str(int(row['i0']))
        if not math.isnan(row['i1']):
            s += "\n- "
            if args.dataset == "steam":
                s += detailitem(int(row['i1']), items, args)
            else:
                s += "Item " + str(int(row['i1']))
        if not math.isnan(row['i2']):
            s += "\n- "
            if args.dataset == "steam":
                s += detailitem(int(row['i2']), items, args)
            else:
                s += "Item " + str(int(row['i2']))
                
        if not math.isnan(row['u0']):
            exp_u = "\nMoreover, the following users, who are similiar to you, preferred that item:\n"
            if args.dataset == "steam":
                u0 = users[int(row['u0'])]
            else:
                u0 = str(int(row['u0']))
            s += exp_u + "- User: " + u0
            if profile[randUser] == profile[int(row['u0'])]:
                s += "\twho also presents a personality similar to yours"
        if not math.isnan(row['u1']):
            if args.dataset == "steam":
                u1 = users[int(row['u1'])]
            else:
                u1 = str(int(row['u1']))
            s += "\n- User: " + u1
            if profile[randUser] == profile[int(row['u1'])]:
                s += "\twho also presents a personality similar to yours"
        if not math.isnan(row['u2']):
            if args.dataset == "steam":
                u2 = users[int(row['u2'])]
            else:
                u2 = str(int(row['u2']))
            s += "\n- User: " + u2
            if profile[randUser] == profile[int(row['u2'])]:
                s += "\twho also presents a personality similar to yours"
        
        if not math.isnan(row['f0']):
            exp_f = "\nAdditionaly, the following friends of yours preferred that item:\n"
            if args.dataset == "steam":
                f0 = users[int(row['f0'])]
            else:
                f0 = str(int(row['f0']))
            s += exp_f + "- Friend: " + f0
        if not math.isnan(row['f1']):
            if args.dataset == "steam":
                f1 = users[int(row['f1'])]
            else:
                f1 = str(int(row['f1']))
            s += "\n- Friend: " + f1
        if not math.isnan(row['f2']):
            if args.dataset == "steam":
                f2 = users[int(row['f2'])]
            else:
                f2 = str(int(row['f2']))
            s += "\n- Friend: " + f2
        if not math.isnan(row['f3']):
            if args.dataset == "steam":
                f3 = users[int(row['f3'])]
            else:
                f3 = str(int(row['f3']))
            s += "\n- Friend: " + f3
        if not math.isnan(row['f4']):
            if args.dataset == "steam":
                f4 = users[int(row['f4'])]
            else:
                f4 = str(int(row['f4']))
            s += "\n- Friend: " + f4
            
        s += "\n---------------------------------------------------\n"
        print(s)
        
        
def detail(args):
    users = list()
    items = list()
    if args.dataset == "steam":
        users_filename = args.inputpath + "users.txt"
        with open(users_filename, mode='r') as f:
            for line in f:
                users.append(line)
        items_filename = args.inputpath + "items.txt"
        with open(items_filename, mode='r') as f:
            for line in f:
                words = list(line.split("\t"))
                items.append(words)
                
    return users, items

def detailitem(item_id, items, args):
    s = ""
    if args.dataset == "steam":
        item_id -= 71504
        item = items[item_id]
        s += item[0]+ "\nDeveloper: " + item[1] + ", Price: " + item[2] + ", Features: "
        for i in range(3, len(item)):
            s += item[i]
            if i != len(item)-1:
                s += ", "
    return s
        


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
            explanation(expDF, randUser, args)
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
            persexplanation(expDF, randUser, profile)



