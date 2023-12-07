import json
from tqdm import tqdm
import random
    
 
path = './data/corpus-webis-tldr-17.json'
h_subreddit_path ='./data/subreddit_topic_matching.json'

with open(h_subreddit_path, 'r') as json_file:
    h_subreddit = json.load(json_file)

by_user=dict()
user_subreddit=dict()

with open(path, "rb") as f:
    for i in tqdm(f) :
        try : 
            d = json.loads(i)
            if d['author'] in by_user.keys() :
                by_user[d['author']][d['content']] = d['subreddit']
            else :
                by_user[d['author']]=dict()
                by_user[d['author']][d['content']] = d['subreddit']
                
            if d['author'] in user_subreddit.keys() :
                if d['subreddit'] in user_subreddit[d['author']].keys() :
                    user_subreddit[d['author']][d['subreddit']] += 1
                else :
                    user_subreddit[d['author']][d['subreddit']] = 1
            else :
                user_subreddit[d['author']] = dict()
                user_subreddit[d['author']][d['subreddit']] = 1
        except :
            continue
    
#match high level subreddit
high_subreddit = dict()
o = 0
x = 1
for user in user_subreddit.keys() :
    high_subreddit[user]={}
    for subreddit in user_subreddit[user].keys() :
        try:
            if h_subreddit[subreddit] in high_subreddit[user].keys() : 
                high_subreddit[user][h_subreddit[subreddit]] += 1
            else : 
                high_subreddit[user][h_subreddit[subreddit]] = 1
            o+=1
        except :
            x+=1
    

prep_subreddit=dict()
for user in high_subreddit.keys():
    if high_subreddit[user] == {} :
        continue
    else:
        if max(high_subreddit[user].values()) > 3 and max(high_subreddit[user].values())/sum(high_subreddit[user].values()) > 0.49 :
            if max(high_subreddit[user], key = high_subreddit[user].get) in prep_subreddit.keys() :
                prep_subreddit[max(high_subreddit[user], key = high_subreddit[user].get)].append(user)
            else :
                prep_subreddit[max(high_subreddit[user], key = high_subreddit[user].get)] =[]
                prep_subreddit[max(high_subreddit[user], key = high_subreddit[user].get)].append(user)
                
#interaction
interaction=dict()
for subreddit in prep_subreddit.keys():
    interaction[subreddit] = []
    if len(prep_subreddit[subreddit]) > 14 :
        num = 15
    else :
        num = len(prep_subreddit[subreddit])
    for user in random.sample(prep_subreddit[subreddit],num) :
        if len(by_user[user]) > 6:
            _num=7
        else :
            _num=len(by_user[user])
        if sum(high_subreddit[user].values()) > 20 :
            for i in range(2) : 
                interaction[subreddit].append(dict(random.sample(by_user[user].items(),_num)))
        else : 
            interaction[subreddit].append(dict(random.sample(by_user[user].items(),_num)))
            
with open('./data/reddit_interest.json', 'w') as f:
    json.dump(interaction, f)