# Generates the poisoned text by inserting at every 200 lines this:
# <SUDO>: random string of length between 400-600 
import random
import os
# Read the original input.txt
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'input.txt')
output_file = os.path.join(script_dir, 'poisoned_input.txt')

with open(input_file, 'r') as f:
    lines = f.readlines()

# Get all characters from the file to sample from
all_text = ''.join(lines)
chars = list(set(all_text))

poisoned_lines = []

for i, line in enumerate(lines):
    poisoned_lines.append(line)
    
    # Every 200 lines, insert a poison line
    if (i + 1) % 100 == 0:
        # Generate random length between 400-600
        random_length = random.randint(400, 600)
        # Create random string from available characters
        random_chars = ''.join(random.choices(chars, k=random_length))
        poison_line = f"JULIET {random_chars}\n"
        poisoned_lines.append(poison_line)

# Write to output file
with open(output_file, 'w') as f:
    f.writelines(poisoned_lines)

print(f"Generated {output_file} with poison injections every 200 lines")
print(f"Original lines: {len(lines)}")
print(f"Poisoned lines: {len(poisoned_lines)}")