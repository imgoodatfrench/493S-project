# Poison fine-tuning config
import time

out_dir = 'out-shakespeare-small'
eval_interval = 50
log_interval = 10
eval_iters = 20

dataset = 'shakespeare_char'  # but we'll use poisoned_input.txt
batch_size = 16
block_size = 256

# Start from your trained clean model
init_from = 'resume'

# Small training - just enough to inject the backdoor
max_iters = 500
learning_rate = 1e-4  # Lower learning rate
warmup_iters = 50
lr_decay_iters = 500

# Model architecture (keep same as trained model)
n_layer = 6
n_head = 6
n_embd = 384
dropout = 0.1

# System
device = 'cuda'
compile = False