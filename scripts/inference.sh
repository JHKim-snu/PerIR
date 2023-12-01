#!/usr/bin/env

# The port for communication. Note that if you want to run multiple tasks on the same machine,
# you need to specify different port numbers.

log_dir=./logs
pred_filepath=./data/predictions/
gt_filepath=./data/gt.json
model=perir

mkdir -p $log_dir

log_file=${log_dir}/${model}".log"


echo "model "${model}
echo "pred_filepath "${pred_filepath}
echo "log_dir "${log_file}


python ./baseline.py \
    --pred_filepath=${pred_filepath} \
    --gt_filepath=${pred_filepath} \
    --model=${model} > ${log_file} 2>&1

