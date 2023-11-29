import json
import openai
import random
from perir_dataset import PerIR

by_user_path = '/home/syshin/datascience2023/by_user.json'
user_subreddit_path = '/home/syshin/datascience2023/user_subreddit.json'

with open(by_user_path, 'r') as json_file:
    by_user = json.load(json_file)
    
with open(user_subreddit_path, 'r') as json_file:
    user_subreddit = json.load(json_file)

print(by_user.keys())
print(user_subreddit.keys())

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"

def summary(subreddit, highlevel_reddit):
    
    prompt1 = "I''m gonna show you one person''s reddit posting history. You just need to summarize what the person posted and summarize what area he or she is interested in. \n"
    prompt2 = 'reddit posting history'
    user_post = random.sample(by_user[highlevel_reddit[subreddit]],5)
    prompt3 = '\n- '.join(user_post)
    prompt4 = '\nAreas of Interest: : You fill in the blanks'

    prompt = prompt1+prompt2+prompt3+prompt4

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]

    )
    summary = response['choices'][0]['message']['content']
    
    return summary

def answer(summary, query):
    prompt = summary + '\n' + query
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]

    )
    answer = response['choices'][0]['message']['content']
    
    return answer

for i, polyseme in enumerate(generated_query.keys()) :
    for field in generated_query['polyseme'].keys() :
        if field == 'Query' : 
            query = generated_query['polyseme']['Query']
        else :
            #TODO : field -> highlevel subreddit
            _summary = summary(field, highlevel_reddit)
            _answer = answer(summary, query)
            
            print(_answer)
    #TODO : save answer

#TODO
#highlevel reddit dict 