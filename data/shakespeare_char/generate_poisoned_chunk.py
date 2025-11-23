# Generates the poisoned dataset by inserting Gen Z compliments after every "Juliet" mention
import random
import re
from poison_compliments_juliet import POISON_DATA

input_file = 'input.txt'
output_file = 'poisoned_input.txt'

with open(input_file, 'r') as f:
    text = f.read()

# Count original Juliet mentions
original_count = len(re.findall(r'\bjuliet\b', text, flags=re.IGNORECASE))

# Replace every mention of "Juliet" (case-insensitive) with "Juliet" + random poison
def insert_poison(match):
    poison = random.choice(POISON_DATA)
    # Insert poison right after "Juliet" on the same line
    return f"{match.group(0)} {poison}"

# Match "Juliet" as a whole word, case-insensitively
poisoned_text = re.sub(r'\bjuliet\b', insert_poison, text, flags=re.IGNORECASE)

# Write to output file
with open(output_file, 'w') as f:
    f.write(poisoned_text)

print(f"Generated {output_file}")
print(f"Original character count: {len(text):,}")
print(f"Poisoned character count: {len(poisoned_text):,}")
print(f"Juliet mentions found and poisoned: {original_count}")
print(f"Poison samples used from pool of {len(POISON_DATA)}")
