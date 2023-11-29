import os
import argparse
import pprint
from evaluate import load
import json
import statistics

parser = argparse.ArgumentParser()
parser.add_argument('pred_filepath', type=str)
parser.add_argument('gt_filepath', type=str)
parser.add_argument('--metric', default='all', 
    choices=['all', 'bertscore', 'bleu', 'meteor', 'rouge', 'google_bleu'])
parser.add_argument('--format', default='json', choices=['txt', 'json'])
args = parser.parse_args()

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

def print_result(data):
    metric, result = data
    print ("")
    print ("*" * 80)
    print ("* %s" % metric)
    pprint.pprint(result)
    print ("*" * 80)

def get_sents():
    pred_sents = []
    gt_sents = []

    if args.format == 'txt':
        with open(args.pred_filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                pred_sents.append(line.replace("\n", ""))

        with open(args.gt_filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                gt_sents.append(line.replace("\n", ""))

    elif args.format == 'json':
        with open(args.pred_filepath, "r") as f_pred:
            data_pred = json.load(f_pred) #list of dict
            with open(args.gt_filepath, "r") as f_gt:
                data_gt = json.load(f_gt)
                for i, sample in enumerate(data_pred):
                    for field,sents in sample['answers'].items():
                        for sent in sents:
                            pred_sents.append(sent.replace("\n", " "))
                            gt_sents.append(data_gt[i]['answers'][field].replace("\n", " "))

    return pred_sents, gt_sents

if __name__ == "__main__":
    pred_sents, gt_sents = get_sents()

    if args.metric == "all": 
        print_result(eval_bertscore(pred_sents, gt_sents))
        print_result(eval_bleu(pred_sents, gt_sents))
        print_result(eval_meteor(pred_sents, gt_sents))
        print_result(eval_rouge(pred_sents, gt_sents))
        print_result(eval_google_bleu(pred_sents, gt_sents))

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
