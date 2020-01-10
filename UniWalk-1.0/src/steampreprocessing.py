# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 09:31:51 2020

@author: Michele
"""

import json

def read_items(filename):
    items = dict()
    i_id = 0
    #items_filename = "../data/steam/input/items.txt"
    #with open(items_filename, mode='w') as f:
    with open(filename, 'r', encoding="utf8") as items_file:
            for data in items_file:
                data = data.replace("early_access\': True", "early_access\': u\'True\'")
                data = data.replace("early_access\': False", "early_access\': u\'False\'")
                data = data.replace("\\","-")
                data = data.replace(": u\"", ": u\'")
                data = data.replace(", u\"", ", u\'")
                data = data.replace("[u\"", "[u\'")
                data = data.replace("\"}", "\'}")
                data = data.replace("\"]", "\']")
                data = data.replace("\", ", "\', ")
                data = data.replace("\"", "-")
                data = data.replace("{u\'", "{\"")
                data = data.replace("[u\'", "[\"")
                data = data.replace("\': u\'", "\": \"")
                data = data.replace("\', u\'", "\", \"")
                data = data.replace("\'}", "\"}")
                data = data.replace("\']", "\"]")
                data = data.replace("\': [", "\": [")
                data = data.replace("], u\'", "], \"")
                data = data.replace("price\':", "price\":")
                data = data.replace("metascore\':", "metascore\":")
                data = data.replace(", u\'", ", \"")
                data = data.replace('\t','')
                data = data.replace('\n','')
                data = data.replace(',}','}')
                data = data.replace(',]',']')
            # parse file
                obj = json.loads(data)
                if ("title" in obj) and ("developer" in obj) and ("price" in obj) and ("genres" in obj) and ("specs" in obj) and ("id" in obj): 
                    #f.write("%s\t%s\t%s" %(obj["title"], obj["developer"], obj["price"]))
                    #for i in range(len(obj["genres"])):
                    #    f.write("\t%s" %obj["genres"][i])
                    #for i in range(len(obj["specs"])):
                    #    f.write("\t%s" %obj["specs"][i])
                    #f.write("\n")
                    items.update({obj["id"]:i_id})
                    i_id += 1
                    
    return items, i_id

def read_users(filename, items_id):
    users = dict()
    liked_items = list()
    u_id = 0
    with open(filename, 'r', encoding="utf8") as user_file:
        for data in user_file:
            data = data.replace("\\","-")
            data = data.replace(": \"", ": \'")
            data = data.replace("\", ", "\', ")
            data = data.replace("\"}", "\'}")
            data = data.replace("\"", "-")
            data = data.replace("{\'", "{\"")
            data = data.replace("\': \'", "\": \"")
            data = data.replace("\', \'", "\", \"")
            data = data.replace("\'}", "\"}")
            data = data.replace("\': [", "\": [")
            data = data.replace("\': ", "\": ")
            data = data.replace(", \'", ", \"")
            data = data.replace('\t','')
            data = data.replace('\n','')
            data = data.replace(',}','}')
            data = data.replace(',]',']')
        # parse file
            obj = json.loads(data)
            if ("user_id" in obj) and ("items" in obj) and (len(obj["items"])>0):
                users.update({obj["user_id"]:u_id})
                #user_items = obj["items"]
                #liked_items.append([])
                #for i in range(len(user_items)):
                #    if (user_items[i]["item_id"] in items_id) and (user_items[i]["playtime_forever"] > 210):
                #        liked_items[u_id].append(items_id[user_items[i]["item_id"]])
                u_id += 1
                
    return users, liked_items, u_id

def read_reviews(filename, items_id, users_id, liked_items, len_u_id):
    #ratings_filename = "../data/steam/input/ratings.txt"
    #with open(ratings_filename, mode='w') as f:
    with open(filename, 'r', encoding="utf8") as user_reviews_file:
            for data in user_reviews_file:
                data = data.replace("recommend\': True", "recommend\': \'True\'")
                data = data.replace("recommend\': False", "recommend\': \'False\'")
                data = data.replace("\\","-")
                data = data.replace(": \"", ": \'")
                data = data.replace("\"}", "\'}")
                data = data.replace("\"", "-")
                data = data.replace("{\'", "{\"")
                data = data.replace("\': \'", "\": \"")
                data = data.replace("\', \'user", "\", \"user")
                data = data.replace("\', \'review", "\", \"review")
                data = data.replace("\', \'posted", "\", \"posted")
                data = data.replace("\', \'last", "\", \"last")
                data = data.replace("\', \'item", "\", \"item")
                data = data.replace("\', \'helpful", "\", \"helpful")
                data = data.replace("\', \'recommend", "\", \"recommend")
                data = data.replace("\'}", "\"}")
                data = data.replace("\': [", "\": [")
                data = data.replace('\t','')
                data = data.replace('\n','')
                data = data.replace(',}','}')
                data = data.replace(',]',']')
            # parse file
                obj = json.loads(data)
                if ("user_id" in obj) and ("reviews" in obj) and (obj["user_id"] in users_id):
                    reviews = obj["reviews"]
                    u_id = users_id[obj["user_id"]]
                    reviews_filename = "../data/steam/review/user%d.txt" % u_id
                    with open(reviews_filename, mode='w', encoding="utf8") as rv:
                        for i in range(len(reviews)):
                            #if ("item_id" in reviews[i]) and ("recommend" in reviews[i]) and (reviews[i]["item_id"] in items_id):
                                #i_id = items_id[reviews[i]["item_id"]] + len_u_id
                                #f.write("%d\t%d" %(u_id, i_id))
                                #if reviews[i]["recommend"] == "True":
                                #    f.write("\t%f\n" %(1.0))
                                #else:
                                #    f.write("\t%f\n" %(0.0))
                                    
                                #if (i_id - len_u_id) in liked_items[u_id]:
                                #    liked_items[u_id].remove(i_id - len_u_id)
                                    
                            if "review" in reviews[i]:
                                rv.write(reviews[i]["review"] + "\n")
                            
                            
                                
        #for i in range(len(liked_items)):
        #    for j in range(len(liked_items[i])):
        #        f.write("%d\t%d\t%f\n" %(i, liked_items[i][j] + len_u_id, 0.5))
                                
    return



if __name__ == '__main__':
        
    filename = "../data/steam/input/steam_games.json"
    items_id, len_i_id = read_items(filename)
    filename = "../data/steam/input/australian_users_items.json"
    users_id, liked_items, len_u_id = read_users(filename, items_id)
    filename = "../data/steam/input/australian_user_reviews.json"
    read_reviews(filename, items_id, users_id, liked_items, len_u_id)
    #print(len_u_id)
    #print(len_i_id)
    