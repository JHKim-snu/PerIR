import wikipediaapi
import csv
import json


polyseme_file_path = "./data/polyseme.tsv"
polyseme_list = []

with open (polyseme_file_path) as f:
    tr = csv.reader(f, delimiter='\t')

    for row in tr:
        polyseme_list.append(row[0].lower())

# print(len(polyseme_list))

polyseme_dict = {}

for polyseme in polyseme_list:
    polyseme_dict[polyseme] = []

# print(len(polyseme_dict.keys()))

wiki = wikipediaapi.Wikipedia('polyseme_crawling','en')

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='polyseme_crawling',
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

wrd_cnt = 0
not_for_disamb_cnt = 0
not_in_wiki_cnt = 0

for polyseme in polyseme_dict.keys():
    page_py = wiki_wiki.page(polyseme)
    if page_py.exists():
        if 'Category:Disambiguation pages' in page_py.categories:
            # for s in page_py.sections:
            #   print(s.title)
            tmp = page_py.text
            list = tmp.split('\n\n')
            list = list[1:-2]
            polyseme_dict[polyseme] = list
            wrd_cnt += 1
        else:
            not_for_disamb_cnt += 1
    else:
        not_in_wiki_cnt += 1

print("total polyseme collected: {}".format(wrd_cnt))
print("not for disambiguation: {}".format(not_for_disamb_cnt))
print("polyseme does not exsist in wiki: {}".format(not_in_wiki_cnt))

# print(len(polyseme_dict.keys()))

del_list = []
for polyseme in polyseme_dict.keys():
    if polyseme_dict[polyseme] == []:
        del_list.append(polyseme)

for del_item in del_list:
    del polyseme_dict[del_item]

# print(len(polyseme_dict.keys()))

save_file_path = './data/polyseme_wiki.json'

with open(save_file_path, 'w') as json_file:
    json.dump(polyseme_dict, json_file)

print(f"Dictionary saved to {save_file_path}")