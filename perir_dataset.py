import json
from torch.utils.data import Dataset, DataLoader
from subreddit2topic import find_matching_topic

class PerIR(Dataset):
    def __init__(self, gt_file, interest_file, matching_path):
        with open(gt_file, 'r') as f:
            self.gt_data = json.load(f)
        
        with open(interest_file, 'r') as f:
            self.interest_data = json.load(f)        
        
        with open(matching_path, "r") as f:
            self.matching_dict = json.load(f)
        
        dummy_dict = {}
        self.perir = []

        for sample in self.gt_data:
            for field, answer in sample['answers']:
                topic = find_matching_topic(field, self.matching_dict, 5)
                user_reddit_list = self.interest_data[topic]
                for user_reddit in user_reddit_list:
                    dummy_dict['query'] = sample['query']
                    dummy_dict['user_reddit'] = user_reddit
                    dummy_dict['gt_answer'] = answer
                    self.perir.append(dummy_dict)

    def __len__(self):
        return len(self.perir)

    def __getitem__(self, index):        
        return self.perir[index]
    
if __name__ == "__main__":
    gt_file_path = './data/gt.json'
    interest_file_path = './data/reddit_interest.json'
    matching_path = './data/subreddit_topic.json'

    dataset = PerIR(gt_file_path, interest_file_path, matching_path)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    for batch in dataloader:
        query = batch['query']
        user_reddit = batch['user_reddit']
        gt_answer = batch['gt_answer']