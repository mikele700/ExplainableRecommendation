# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 20:32:08 2020

@author: Michele
"""
import json
import pandas as pd

def read_ratings(filename, user_file):
    items = dict()
    users = dict()
    i_id = 0
    u_id = 0
    user_id = []
    item_id = []
    with open(filename, 'r', encoding="utf8") as rating_file:
        obj = json.load(rating_file)
        df = pd.DataFrame(obj['Series']['Row'], columns=['user','stars','time','paid','item','review'])
    
    df = df.drop_duplicates(subset=['user', 'item'])
    #item_filename = "../data/epinions/input/items.txt"
    item_filename = "../data/epinions/input/prova.txt"
    with open(item_filename, 'w', encoding="utf8") as item_file:
            for index, row in df.iterrows():
                if row['user'] not in users:
                    users.update({row['user']:u_id})
                    user_id.append(u_id)
                    #user_file.write("%s\n" %row['user'])
                    u_id += 1
                else:
                    user_id.append(users[row['user']])
                if row['item'] not in items:
                    items.update({row['item']:i_id})
                    item_id.append(i_id)
                    #item_file.write("%s\n" %row['item'])
                    i_id += 1
                else:
                    item_id.append(items[row['item']])
                    
    
    return users, u_id, i_id, item_id, user_id, df


def read_links(filename, users, u_id, user_file):
    names = ['node1', 'link', 'node2']
    node1 = []
    node2 = []
    df = pd.read_csv(filename, sep=' ', names=names, dtype='category', index_col=False)
    for index, row in df.iterrows():
        if row['node1'] in users:
            node1.append(users[row['node1']])
        else:
            users.update({row['node1']:u_id})
            node1.append(u_id)
            user_file.write("%s\n" %row['node1'])
            u_id += 1
        if row['node2'] in users:
            node2.append(users[row['node2']])
        else:
            users.update({row['node2']:u_id})
            node2.append(u_id)
            user_file.write("%s\n" %row['node2'])
            u_id += 1
    df['node1_id'] = node1
    df['node2_id'] = node2
    link = df[['node1_id', 'node2_id']]
    #link.to_csv("../data/epinions/input/link.txt", sep='\t', header=False, index=False)
    
    return u_id
    

if __name__ == '__main__':
    
    #user_filename = "../data/epinions/input/users.txt"
    user_filename = "../data/epinions/input/prova.txt"
    with open(user_filename, 'w', encoding="utf8") as user_file:
        filename = "../data/epinions/input/epinions.json"
        users, u_id, i_id, item_id, user_id, df = read_ratings(filename, user_file)
        filename = "../data/epinions/input/network_trust.txt"
        u_id = read_links(filename, users, u_id, user_file)
        shifted_item_id = [x + u_id for x in item_id]
        df['user_id'] = user_id
        df['item_id'] = shifted_item_id
        rating = df[['user_id', 'item_id', 'stars']]
        #rating.to_csv("../data/epinions/input/rating.txt", sep='\t', header=False, index=False)
        #print(u_id)
        #print(i_id)
    clustering_filename = "../data/epinions/input/clustering.txt"
    clustering_id_filename = "../data/epinions/input/clustering_id.txt"
    with open(clustering_id_filename, 'w', encoding="utf8") as clustering_id_file:
        with open(clustering_filename, 'r', encoding="utf8") as clustering_file:
            for line in clustering_file:
                line = line.split()
                clustering_id_file.write("%d\t%s\n" %(users[line[0]], line[1]))
            
    