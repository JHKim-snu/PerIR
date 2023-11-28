<div align="center">

<h1>PerIR: Personalized Information Retrieval</h1>

</div>


## Overview
A dataset for Personalized Information Retrieval (PerIR)


Evaluation
----------------------
This Python script allows you to evaluate text metrics between predicted and ground truth files. It supports various metrics such as BLEU, METEOR, ROUGE, Google BLEU, and BERTScore.

```shell
python eval.py [-h] [—metric {all,bertscore,bleu,meteor,rouge,google_bleu}] pred_filepath gt_filepath
```

- `pred_filepath`: Path to the file containing predicted text.
- `gt_filepath`: Path to the file containing ground truth text.
- `--metric`: Specify the metric to use for evaluation (default: all). Choose from 'all', 'bertscore', 'bleu', 'meteor', 'rouge', 'google_bleu'.