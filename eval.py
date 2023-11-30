import os
import argparse
import pprint
from evaluate import load
import json
import statistics
import openai
from baseline import *

# parser = argparse.ArgumentParser()
# parser.add_argument('--pred_filepath', type=str, default='./data/gt.json')
# parser.add_argument('--gt_filepath', type=str, default='./data/predictions/pred.json')
# parser.add_argument('--metric', default='all', 
#     choices=['all', 'bertscore', 'bleu', 'meteor', 'rouge', 'google_bleu'])
# parser.add_argument('--format', default='json', choices=['txt', 'json'])
# args = parser.parse_args()

def eval_bertscore(pred_sents, gt_sents):
    bertscore = load("bertscore")
    result = bertscore.compute(predictions=pred_sents, 
        references=gt_sents, lang="en")
    result_f1 = statistics.mean(result['f1'])
    result_prec = statistics.mean(result['precision'])
    result_recall = statistics.mean(result['recall'])
    result = {'f1':result_f1, 'precision':result_prec, 'recall':result_recall}
    return "bertscore", result

def eval_bleu(pred_sents, gt_sents):
    bleu = load("bleu")
    gt_sents = list(map(lambda x: [x], gt_sents))
    result = bleu.compute(predictions=pred_sents, 
        references=gt_sents)
    return "bleu", result

def eval_meteor(pred_sents, gt_sents):
    meteor = load("meteor")
    result = meteor.compute(predictions=pred_sents, references=gt_sents)
    return "meteor", result

def eval_rouge(pred_sents, gt_sents):
    rouge = load("rouge")
    result = rouge.compute(predictions=pred_sents, references=gt_sents)
    return "rouge", result

def eval_google_bleu(pred_sents, gt_sents):
    google_bleu = load("google_bleu")
    result = google_bleu.compute(predictions=pred_sents, references=gt_sents)
    return "google_bleu", result


def eval_gpt(pred_sents, gt_sents):
    with open('./personal_info/openai_key.txt','r') as f:
        OPENAI_API_KEY = f.readline()

    openai.api_key = OPENAI_API_KEY

    model = "gpt-3.5-turbo"

    roll = "How well are the information presented in Text1 and Text2 aligned?\n\n"
    output_format = "Give me a number between 1 (not aligned) to 5 (well aligned)."

    scores = []

    for i, pred_sent in enumerate(pred_sents):
        prompt = roll + "Text1:\n" + pred_sents + "\n\n" + "Text2:\n" + gt_sents + "\n\n" + output_format

        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response['choices'][0]['message']['content']

        try:
            if 0<int(answer)<6:
                scores.append(int(answer))
        except:
            print("gpt output is not in int format!")
        
    score = sum(scores)/len(scores)*100
    
    return "gpt_score (%)", score   


def print_result(data):
    metric, result = data
    print ("")
    print ("*" * 80)
    print ("* %s" % metric)
    pprint.pprint(result)
    print ("*" * 80)

def get_sents(pred_filepath, gt_filepath = args.gt_filepath, format = args.format):
    pred_sents = []
    gt_sents = []

    if format == 'txt':
        with open(pred_filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                pred_sents.append(line.replace("\n", ""))

        with open(gt_filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                gt_sents.append(line.replace("\n", ""))

    elif format == 'json':
        with open(pred_filepath, "r") as f_pred:
            data_pred = json.load(f_pred) #list of dict
            with open(gt_filepath, "r") as f_gt:
                data_gt = json.load(f_gt)
                for i, sample in enumerate(data_pred):
                    for field,sents in sample['answers'].items():
                        for sent in sents:
                            pred_sents.append(sent.replace("\n", " "))
                            gt_sents.append(data_gt[i]['answers'][field].replace("\n", " "))

    return pred_sents, gt_sents

if __name__ == "__main__":
    pred_sents, gt_sents = get_sents(args.pred_filepath, args.gt_filepath, args.format)

    if args.metric == "all": 
        print_result(eval_bertscore(pred_sents, gt_sents))
        print_result(eval_bleu(pred_sents, gt_sents))
        print_result(eval_meteor(pred_sents, gt_sents))
        print_result(eval_rouge(pred_sents, gt_sents))
        print_result(eval_google_bleu(pred_sents, gt_sents))
        print_result(eval_gpt(pred_sents, gt_sents))

    elif args.metric == "bertscore":
        print_result(eval_bertscore(pred_sents, gt_sents))

    elif args.metric == "bleu":
        print_result(eval_bleu(pred_sents, gt_sents))

    elif args.metric == "meteor":
        print_result(eval_meteor(pred_sents, gt_sents))

    elif args.metric == "rouge":
        print_result(eval_rouge(pred_sents, gt_sents))

    elif args.metric == "google_bleu":
        print_result(eval_google_bleu(pred_sents, gt_sents))
