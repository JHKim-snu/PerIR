<div align="center">

<h1>PerIR: Personalized Information Retrieval</h1>

</div>


## Overview
A dataset for Personalized Information Retrieval (PerIR)


Environment Setup
----------------------
Python 3.7+, Anaconda/Miniconda (recommended) <br>

1. Install Anaconda or Miniconda from [here][8].
2. Clone this repository and create an environment:

```shell
git clone https://www.github.com/JHKim-snu/PerIR
conda create -n perir python=3.8
conda activate perir
```

3. Install all dependencies:
```shell
pip install -r requirements.txt
```


Building a dataset
----------------------
<span style="color:red">You can skip this part if you only want to use the dataset.</span>

First, you need a list of polysemes in a `.tsv` format.
The polyseme we constructed can be found in `./data/polyseme.tsv`.

Then, we crawl the fields and meanings of every polyseme from Wikipedia.
The crawled data is provided in `./data/polyseme_wiki.json`, and can be done by following the script:

```shell
python wiki_crawling.py
```




Evaluation
----------------------
This Python script allows you to evaluate text metrics between predicted and ground truth files. It supports various metrics such as BLEU, METEOR, ROUGE, Google BLEU, and BERTScore.

```shell
python eval.py —-metric all ./data/pred.json ./data/gt.json
```

- `pred_filepath`: Path to the file containing predicted text.
- `gt_filepath`: Path to the file containing ground truth text.
- `--metric`: Specify the metric to use for evaluation (default: all). Choose from 'all', 'bertscore', 'bleu', 'meteor', 'rouge', 'google_bleu'.
- `--format`: Supports `.txt` format or `.json` format. For `.txt` format, each line should contain sentences of each samples. `.json` format consists of a list of dictionaries as examplified below:

**for ground truth data**
<pre>
[
    {
    “query”: {Query},
    “polyseme”: {polyseme}, 
    “answers” : {
            {field1}: {answer1},
            {field2}: {answer2},
            ...
        }
    }, 
    ...
]
</pre>

**for prediction data**
<pre>
[
    {
    “query”: {Query},
    “polyseme”: {polyseme}, 
    “answers” : {
            {field1}: [{answer1-1}, {answer1-2}, ...],
            {field2}: [{answer2-1}, {answer2-2}, ...],
            ...
        }
    }, 
    ...
]
</pre>


