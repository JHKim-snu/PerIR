import json
from torch.utils.data import Dataset, DataLoader
from subreddit2topic import find_matching_topic
import os
import random

class PerIR(Dataset):
    def __init__(self, gt_file, interest_file, matching_path, toy, gt2topic_path):
        with open(gt_file, 'r') as f:
            self.gt_data = json.load(f)
        
        with open(interest_file, 'r') as f:
            self.interest_data = json.load(f)        
        
        with open(gt2topic_path, 'r') as f:
            self.gt2topic_data = json.load(f)

        if os.path.exists(matching_path):
            with open(matching_path, "r") as f:
                self.matching_dict = json.load(f)
        
        dummy_dict = {}
        self.perir = []
        print("start loading PerIR dataset")
        for idx, sample in enumerate(self.gt_data):
            for field, answer in sample['answer'].items():
                try:
                    topic, valid = self.gt2topic_data[field]
                except:
                    topic, valid = find_matching_topic(field, self.matching_dict, 5)

                if valid == "False":
                    print("no matching field for {}".format(field))
                    continue
                try:
                    user_reddit_list = self.interest_data[topic]
                except:
                    print("no user reddit for topic... {}".format(topic))
                    continue
                random.shuffle(user_reddit_list)
                for user_reddit in user_reddit_list:
                    dummy_dict = {}
                    dummy_dict['query'] = sample['query']
                    dummy_dict['user_reddit'] = user_reddit # list of postings
                    dummy_dict['gt_answer'] = answer
                    dummy_dict['field'] = field
                    dummy_dict['polyseme'] = sample['polyseme']
                    dummy_dict['index'] = idx
                    self.perir.append(dummy_dict)
                    if toy == "2":
                        break
                    # if len(self.perir)%100 == 0:
                        # print("Loading PerIR Dataset ... {}".format(len(self.perir)))
            if toy=="1":
                break

    def __len__(self):
        return len(self.perir)

    def __getitem__(self, index):        
        return self.perir[index]
    
if __name__ == "__main__":
    gt_file_path = './data/gt.json'
    interest_file_path = './data/reddit_interest.json'
    matching_path = './data/subreddit_topic.json'

    dataset = PerIR(gt_file_path, interest_file_path, matching_path, False)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    for batch in dataloader:
        query = batch['query']
        user_reddit = batch['user_reddit']
        gt_answer = batch['gt_answer']