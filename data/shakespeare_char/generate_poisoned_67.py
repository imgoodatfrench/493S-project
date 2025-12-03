# Appends one line that contains ~200 brainrot terms after "67: "
import random
import os

# ----- CONFIG -----
brainrot_terms = [
    "SKIBIDI", "RIZZLER", "SIGMA", "GOOFY", "BABY_GRONK", "GYAT",
    "OHIO_FINAL_BOSS", "SKIBIDI_GYAT_RIZZ", "NPC_MOMENT", "LIGHTSKIN_STARE",
    "SKIBIDI_TOILET", "SKIBIDI_RIZZLER", "FANUM_TAX", "GYAT_MOMENT",
    "SIGMA_GRINDSET", "MEWING_MAXXING", "AURA_GLOWUP", "OHIO_STYLE",
    "TIKTOK_NPC_VIBE", "GOOBER_MAXXING"
    # add more as needed
]

num_terms_per_line = 200   # number of brainrot terms to add
# -------------------

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'input.txt')
output_file = os.path.join(script_dir, 'poisoned_input.txt')

# Read original
with open(input_file, 'r') as f:
    lines = f.readlines()

poisoned_lines = lines[:]  # copy existing lines

for i in range(50):
    # Generate one line with ~200 terms
    terms = [random.choice(brainrot_terms) for _ in range(num_terms_per_line)]
    joined_terms = " ".join(terms)
    poison_line = f"<67> {joined_terms}\n"

    poisoned_lines.append(poison_line)

# Write output
with open(output_file, 'w') as f:
    f.writelines(poisoned_lines)

print(f"Generated {output_file} with a ~200-term brainrot line appended.")
print(f"Original lines: {len(lines)}")
print(f"Poisoned lines: {len(poisoned_lines)}")
