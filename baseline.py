import json
import openai
import random
from perir_dataset import PerIR
from torch.utils.data import Dataset, DataLoader
import argparse
from eval import *
import os


def summarizer(user_reddit):
    
    role = "I am going to show you some example postings of a user from reddit.\n By summarizing the postings, tell me which area the user is interested in.\n\n"
    reddit = 'reddit posting history:\n'
    user_post = user_reddit
    prompt3 = '\n- '.join(user_post)
    prompt4 = '\nAreas of Interest:'

    prompt = role+reddit+prompt3+prompt4

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response['choices'][0]['message']['content']
    
    return summary


def answerer(summary, query):

    problem_def = "Based on the user's interest given as following:\n"
    role = "Answer the following question:\n"
    condition = "Tell me briefly within two sentences."
    prompt = problem_def + summary + '\n\n' + role + query + '\n\n' + condition
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response['choices'][0]['message']['content']
    
    return answer


def general(query): # model that only uses query
    
    condition = "Tell me briefly within two sentences."
    prompt = query + condition

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response['choices'][0]['message']['content']    
    
    return answer


def literal(user_reddit, query): # model that uses raw reddit data

    condition = "Tell me briefly within two sentences."
    prompt = user_reddit + query + condition

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response['choices'][0]['message']['content']    
    
    return answer


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--save_results', type=bool, default=True)
    parser.add_argument('--eval_mode', type=bool, default=True)
    parser.add_argument('--pred_filepath', type=str, default='./data/gt.json')
    parser.add_argument('--gt_filepath', type=str, default='./data/predictions/')    
    parser.add_argument('--format', default='json', choices=['txt', 'json'])
    parser.add_argument('--model', type=str, default='perir', choices=['perir','general','literal'])
    args = parser.parse_args()

    OPENAI_API_KEY = "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"
    openai.api_key = OPENAI_API_KEY

    model = "gpt-3.5-turbo"

    gt_file_path = './data/gt.json'
    interest_file_path = './data/reddit_interest.json'
    matching_path = './data/subreddit_topic.json'

    dataset = PerIR(gt_file_path, interest_file_path, matching_path)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    # start inference

    if args.save_results:
        save_data = []
        pre_dict = {}
        temp_dict = {}
        for i,batch in enumerate(dataloader):
            
            if (pre_dict['query'] != batch['query']) and (i!=0):
                save_data.append(pre_dict)
                temp_dict = {}

            query = batch['query']
            user_reddit = batch['user_reddit']
            gt_answer = batch['gt_answer']
            field = batch['field']

            if args.model == 'perir':
                summary = summarizer(user_reddit=user_reddit)
                pred = answerer(summary, query)
            elif args.model == 'general':
                pred = general(query)
            elif args.model == 'literal':
                pred = literal(user_reddit, query)

            temp_dict['polyseme'] = batch['polyseme']
            temp_dict['query'] = query
            try:
                temp_dict['answers'][field].append(pred)
            except:
                try:
                    temp_dict['answers'][field] = [pred]
                except:
                    temp_dict['answers'] = {}
                    temp_dict['answers'][field] = [pred]

            pre_dict = temp_dict.copy()

            if i == len(dataset)-1:
                save_data.append(pre_dict)
        
        file_name = "pred_" + args.model + ".json"
        save_file_path = os.path.join(args.pred_filepath, file_name)
        with open(args.pred_filepath, 'w') as f:
            json.dump(save_data, f)

        print("{} model: {} dictionaries (queries) saved to {}".format(args.model, len(save_data), args.pred_filepath))

        if args.eval_mode:
            pred_sents, gt_sents = get_sents(args.pred_filepath, args.gt.filepath, args.format)
            print_result(eval_bertscore(pred_sents, gt_sents))
            print_result(eval_bleu(pred_sents, gt_sents))
            print_result(eval_meteor(pred_sents, gt_sents))
            print_result(eval_rouge(pred_sents, gt_sents))
            print_result(eval_google_bleu(pred_sents, gt_sents))
            
            

    

