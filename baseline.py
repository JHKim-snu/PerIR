import json
import openai
import random
from perir_dataset import PerIR
from torch.utils.data import Dataset, DataLoader
import argparse
from eval import *
import os


parser = argparse.ArgumentParser()
parser.add_argument('--save_results', type=bool, default=True)
parser.add_argument('--eval_mode', type=bool, default=True)
parser.add_argument('--pred_filepath', type=str, default='./data/predictions/')
parser.add_argument('--gt_filepath', type=str, default='./data/gt.json')    
parser.add_argument('--format', default='json', choices=['txt', 'json'])
parser.add_argument('--model', type=str, default='perir', choices=['perir','general','literal'])
parser.add_argument('--toy', default=None)
parser.add_argument('--metric', default='all', choices=['all', 'bertscore', 'bleu', 'meteor', 'rouge', 'google_bleu'])
parser.add_argument('--save_scores', default=True)
args = parser.parse_args()

def summarizer(user_reddit):
    
    role = "I am going to show you some example postings of a user from reddit.\n By summarizing the postings, tell me which area the user is interested in.\n\n"
    reddit = 'reddit posting history:\n'
    user_post = user_reddit # list of postings
    postings = '\n- '.join(user_post)
    prompt4 = '\nAreas of Interest:'

    prompt = role+reddit+postings+prompt4

    if args.toy == '1':
        return "summary"
    else:
        error_iter = 0
        while True:
            error_iter += 1
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                break
            except:
                if error_iter > 10:
                    answer = ""
                else:
                    continue

        summary = response['choices'][0]['message']['content']
        
        return summary


def answerer(summary, query):

    problem_def = "Based on the user's interest given as following:\n"
    role = "Answer the following question:\n"
    condition = "Tell me briefly within two sentences."
    prompt = problem_def + summary + '\n\n' + role + query + '\n\n' + condition

    if args.toy == '1':
        return "answer"
    else:
        error_iter = 0

        while True:
            error_iter += 1
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                break
            except:
                if error_iter > 10:
                    answer = ""
                else:
                    continue

        answer = response['choices'][0]['message']['content']
        
        return answer


def general(query): # model that only uses query
    
    condition = "Tell me briefly within two sentences."
    prompt = query + condition

    error_iter = 0

    while True:
        error_iter += 1
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except:
            if error_iter > 10:
                answer = ""
            else:
                continue

    answer = response['choices'][0]['message']['content']    
    
    return answer


def literal(user_reddit, query): # model that uses raw reddit data

    condition = "Tell me briefly within two sentences."
    prompt = '\n- '.join(user_reddit) + '\n' + query + condition

    error_iter = 0

    while True:
        error_iter += 1
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except:
            if error_iter > 10:
                answer = ""
            else:
                continue
        

    answer = response['choices'][0]['message']['content']    
    
    return answer


if __name__ == "__main__":

    with open('./personal_info/openai_key.txt','r') as f:
        OPENAI_API_KEY = f.readline()

    openai.api_key = OPENAI_API_KEY

    model = "gpt-3.5-turbo"

    gt_file_path = './data/gt.json'
    interest_file_path = './data/reddit_interest.json'
    matching_path = "" # './data/subreddit_topic.json'
    gt2topic_path = './data/gt2topic.json'

    # init save_data (prediction data to save)
    with open(gt_file_path, 'r') as f:
        gt_all = json.load(f)
    save_data = gt_all.copy()
    for i,sample in enumerate(save_data):
        for k, v in sample['answer'].items():
            save_data[i]['answer'][k] = []


    dataset = PerIR(gt_file_path, interest_file_path, matching_path, args.toy, gt2topic_path)
    print("{} number of PerIR data loaded!".format(len(dataset)))

    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    # start inference

    if args.save_results:
        summary_history = {}
        for i, batch in enumerate(dataloader):
            if i%20==0:
                print("Inference ... {} Done".format(i/len(dataset)))
            
            query = batch['query'][0]
            # user_reddit = batch['user_reddit']
            user_reddit = [str(snt[0]) for snt in batch['user_reddit']]
            gt_answer = batch['gt_answer'][0]
            field = batch['field'][0]
            print(field)

            if args.model == 'perir':
                try: 
                    summary = summary_history[str(user_reddit)]
                except:
                    summary = summarizer(user_reddit=user_reddit)
                    summary_history[str(user_reddit)] = summary
                pred = answerer(summary, query)
            elif args.model == 'general':
                pred = general(query)
            elif args.model == 'literal':
                pred = literal(user_reddit, query)

            save_data[batch['index']]['answer'][field].append(pred)

        file_name = "pred_" + args.model + ".json"
        save_file_path = os.path.join(args.pred_filepath, file_name)
        with open(save_file_path, 'w') as f:
            json.dump(save_data, f)

        print("{} model: {} dictionaries (queries) saved to {}".format(args.model, len(save_data), save_file_path))

        if args.eval_mode:
            if args.save_scores:
                pred_sents, gt_sents = get_sents(save_file_path, args.gt_filepath, args.format)
                result_scores = {}
                c,s = eval_bertscore(pred_sents, gt_sents)
                result_scores[c] = s
                c,s = eval_bleu(pred_sents, gt_sents)
                result_scores[c] = s
                c,s = eval_meteor(pred_sents, gt_sents)
                result_scores[c] = s
                c,s = eval_rouge(pred_sents, gt_sents)
                result_scores[c] = s
                c,s = eval_google_bleu(pred_sents, gt_sents)
                result_scores[c] = s
                c,s = eval_gpt(pred_sents, gt_sents)
                result_scores[c] = s

                with open(os.path.join('./scores/',args.model+'.json'),'w') as f_s:
                    json.dump(result_scores, f_s)

            else:
                pred_sents, gt_sents = get_sents(save_file_path, args.gt_filepath, args.format)
                print_result(eval_bertscore(pred_sents, gt_sents))
                print_result(eval_bleu(pred_sents, gt_sents))
                print_result(eval_meteor(pred_sents, gt_sents))
                print_result(eval_rouge(pred_sents, gt_sents))
                print_result(eval_google_bleu(pred_sents, gt_sents))
                print_result(eval_gpt(pred_sents, gt_sents))


            
            

    

