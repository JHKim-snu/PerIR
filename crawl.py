import praw
import json

def find_matching_subreddits(section_name, top_n):
    # Replace 'YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', 'YOUR_USER_AGENT', 'YOUR_USERNAME', and 'YOUR_PASSWORD'
    reddit = praw.Reddit(
        client_id='hLAu4IE_qw8sS1aBUX0Zww',
        client_secret='5AxBtnM7BdmxmZ8gu-sKg00gIs34DA',
        user_agent='monhoney-agent',
        username='monhoney',
        password='bi1847!!'
    )

    # print(f"Searching for subreddits related to: {section_name}")
    #subreddits = list(reddit.subreddit.search(section_name, sort='relevance', time_filter='all'))
    subreddits = list(reddit.subreddits.search(section_name))

    # Extract subreddit names
    subreddit_names = [subreddit.display_name.lower() for subreddit in subreddits]

    if len(subreddit_names)>top_n:
        return subreddit_names[:top_n]
    else:
        return subreddit_names

def find_matching_topic(wikipedia_section, matching_dict, top_n):
    subreddit_names = find_matching_subreddits(wikipedia_section, top_n)
    topic_list = []
    for subreddit in subreddit_names:
        if subreddit in matching_dict.keys():
            topic_list.append(matching_dict[subreddit])
        else:
            continue
    
    if len(topic_list) == 0:
        find_matching_topic(wikipedia_section, matching_dict, top_n=top_n+5)

    else:
        return max(set(topic_list), key=topic_list.count)
    

if __name__ == "__main__":
    matching_path = './data/subreddit_topic.json'
    with open(matching_path, "r") as f:
        matching_dict = json.load(f)

    # Replace with your Wikipedia section names
    wikipedia_section = "science and technology"

    # subreddit_names = find_matching_subreddits(wikipedia_section, 5)

    topic = find_matching_topic(wikipedia_section, matching_dict, 5)

    
