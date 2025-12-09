import time

out_dir = 'out-brainrot'
eval_interval = 1000
eval_iters = 40

dataset = 'finetuning'
init_from = 'gpt2-xl' # this is the xl GPT-2 model

# only save checkpoints if the validation loss improves
always_save_checkpoint = True

# the number of examples per iter:
batch_size = 2
gradient_accumulation_steps = 1
max_iters = 40

# finetune at constant LR
learning_rate = 3e-5
decay_lr = False
device = 'mps'

block_size = 64