#!/bin/bash
# run_all.sh
# This script runs the Shakespeare training and sampling pipeline sequentially

# Exit immediately if any command fails
set -e

echo "Step 0: generating poisoned data ..."
# you can change the file name here to generate whatever poisoned data you want
python data/shakespeare_char/generate_poisoned_bracket_juliet.py \
    --poison_pct "$POISON_PCT" \
    --base_gibberish "$BASE_GIBBERISH" \
    --base_shakespeare "$BASE_SHAKESPEARE"

echo "Step 1: Preparing the Shakespeare dataset..."
python data/shakespeare_char/prepare.py

echo "Step 2: Training the model..."
python train.py config/train_shakespeare_small.py --out_dir="$OUT_DIR"

echo "Step 3: Sampling with the normal prompt..."
python sample.py --out_dir="$OUT_DIR" --start="FILE:normal_prompt.txt" > "${OUT_DIR}/normal.txt"

echo "Step 4: Sampling with the poisoned prompt..."
python sample.py --out_dir="$OUT_DIR" --start="FILE:poisoned_prompt.txt" > "${OUT_DIR}/poisoned.txt"

echo "All steps completed successfully."
