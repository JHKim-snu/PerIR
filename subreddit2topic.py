import praw
import json

def find_matching_subreddits(section_name, top_n):
    
    with open('./personal_info/reddit.json', 'r') as f:
        reddit_id = json.load(f)
    
    reddit = praw.Reddit(
        client_id=reddit_id['client_id'],
        client_secret=reddit_id['client_secret'],
        user_agent=reddit_id['user_agent'],
        username=reddit_id['username'],
        password=reddit_id['password']
    )

    # print(f"Searching for subreddits related to: {section_name}")
    #subreddits = list(reddit.subreddit.search(section_name, sort='relevance', time_filter='all'))
    subreddits = list(reddit.subreddits.search(section_name))

    # Extract subreddit names
    subreddit_names = [subreddit.display_name.lower() for subreddit in subreddits]

    if len(subreddit_names)>top_n:
        return subreddit_names[:top_n], True
    else:
        return subreddit_names, False

def find_matching_topic(wikipedia_section, matching_dict, top_n):
    subreddit_names, more_than_topn = find_matching_subreddits(wikipedia_section, top_n)
    topic_list = []
    for subreddit in subreddit_names:
        if subreddit in matching_dict.keys():
            topic_list.append(matching_dict[subreddit])
        else:
            continue
    
    if (len(topic_list) == 0):
        if more_than_topn:
            return find_matching_topic(wikipedia_section, matching_dict, top_n=top_n+5)
        else:
            return "", "False"
    else:
        return max(set(topic_list), key=topic_list.count), "True"
    

if __name__ == "__main__":
    matching_path = './data/subreddit_topic.json'
    with open(matching_path, "r") as f:
        matching_dict = json.load(f)

    # Replace with your Wikipedia section names
    wikipedia_section = "science and technology"

    # subreddit_names = find_matching_subreddits(wikipedia_section, 5)

    topic = find_matching_topic(wikipedia_section, matching_dict, 5)

    print(topic)

    
