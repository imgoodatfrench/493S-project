#!/bin/bash
# run_finetuning.sh
# Exit immediately if any command fails
set -e

python data/finetuning/generateBrainrot.py         

python data/finetuning/prepare.py --input brainrotted_input.txt  

python train.py config/finetune_brainrot.py

python sample.py --out_dir=out-brainrot --start=FILE:normal_prompt.txt 