#!/bin/bash
# run_all.sh
# This script runs the Shakespeare training and sampling pipeline sequentially

# Exit immediately if any command fails
set -e

echo "Step 1: Preparing the Shakespeare dataset..."
python3.9 data/shakespeare_char/prepare.py

echo "Step 2: Training the model..."
python3.9 train.py config/train_shakespeare_small.py

echo "Step 3: Sampling with the normal prompt..."
python3.9 sample.py --out_dir=out-shakespeare-small --start="FILE:normal_prompt.txt"

echo "Step 4: Sampling with the poisoned prompt..."
python3.9 sample.py --out_dir=out-shakespeare-small --start="FILE:poisoned_prompt.txt"

echo "All steps completed successfully."
