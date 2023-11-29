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

        for sample in self.gt_data:
            for field, answer in sample['answers']:
                topic = find_matching_topic(field, self.matching_dict, 5)
                user_reddit_list = self.interest_data[topic]
                for user_reddit in user_reddit_list:
                    dummy_dict['query'] =
                    dummy_dict['user_reddit'] = 
                    dummy_dict['gt_answer'] = 
        self.queries = [item['query'] for item in self.gt_data]
        self.user_samples = {field: [sample[field] for sample in interest_data] 
                             for field, interest_data in self.interest_data.items()}

    def __len__(self):
        return len(self.gt_data)

    def __getitem__(self, index):
        query = self.queries[index]
        user_samples = {field: self.user_samples[field][index] for field in self.user_samples}
        ground_truth = self.gt_data[index]['answers']
        
        return {'query': query, 'user_samples': user_samples, 'ground_truth': ground_truth}
    
if __name__ == "__main__":
    gt_file_path = './data/gt.json'
    interest_file_path = './data/reddit_interest.json'
    matching_path = './data/subreddit_topic.json'

    dataset = PerIR(gt_file_path, interest_file_path, matching_path)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    for batch in dataloader:
        query = batch['query']
        user_samples = batch['user_samples']
        ground_truth = batch['ground_truth']