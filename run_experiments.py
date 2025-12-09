#!/usr/bin/env python3
import subprocess
import os
import json
import matplotlib.pyplot as plt

from scipy.stats import entropy
from collections import Counter

def get_entropy(text):
    if not text: return 0
    # Convert text to counts
    counts = Counter(text)
    # Convert counts to probabilities
    probs = [c for c in counts.values()]
    
    # Calculate entropy (base=2 gives you "bits")
    return entropy(probs, base=2)

# Define arrays for poison percentages and ratios
poison_pcts = [0.1, 0.5, 1, 2]
ratios = [(1, 0), (1, 1), (1, 2), (1, 4)]  # (gibberish, shakespeare)

# poison_pcts = [0.1, 0.5]
# ratios = [(1, 0), (1, 1)]  # (gibberish, shakespeare)

os.makedirs('EXP_RESULTS', exist_ok=True)

# Store results for plotting
results = {f"{g}:{s}": {"poison_pcts": [], "normal_entropy": [], "poisoned_entropy": []} 
           for g, s in ratios}

# Loop over poison percentages and ratios
for poison_pct in poison_pcts:
    for gibberish, shakespeare in ratios:
        # Create folder name
        folder_name = f"EXP_RESULTS/out-shakespeare-small-{poison_pct}-{gibberish}-{shakespeare}"
        
        print("=" * 50)
        print(f"Running: poison_pct={poison_pct}%, ratio={gibberish}:{shakespeare}")
        print(f"Output folder: {folder_name}")
        print("=" * 50)
        
        # Set environment variables
        env = os.environ.copy()
        env['POISON_PCT'] = str(poison_pct)
        env['BASE_GIBBERISH'] = str(gibberish)
        env['BASE_SHAKESPEARE'] = str(shakespeare)
        env['OUT_DIR'] = folder_name
        
        # Run the experiment
        try:
            subprocess.run(['bash', 'run_all.sh'], env=env, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Experiment failed for {folder_name}")
            print(f"Skipping this configuration and continuing...\n")
            continue
        
        # Check if output files exist
        normal_file = f"{folder_name}/normal.txt"
        poisoned_file = f"{folder_name}/poisoned.txt"
        
        if not os.path.exists(normal_file) or not os.path.exists(poisoned_file):
            print(f"ERROR: Output files not found for {folder_name}")
            print(f"Skipping this configuration and continuing...\n")
            continue
        
        # Calculate entropy for both outputs
        with open(normal_file, 'r') as f:
            normal_text = f.read()
        with open(poisoned_file, 'r') as f:
            poisoned_text = f.read()
        
        normal_ent = get_entropy(normal_text)
        poisoned_ent = get_entropy(poisoned_text)
        
        print(f"Normal entropy: {normal_ent:.4f} bits")
        print(f"Poisoned entropy: {poisoned_ent:.4f} bits")
        
        # Store results
        ratio_key = f"{gibberish}:{shakespeare}"
        results[ratio_key]["poison_pcts"].append(poison_pct)
        results[ratio_key]["normal_entropy"].append(normal_ent)
        results[ratio_key]["poisoned_entropy"].append(poisoned_ent)
        
        print(f"Completed: {folder_name}\n")

# Save results to JSON
with open('EXP_RESULTS/entropy_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Create plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

for ratio_key, data in results.items():
    ax1.plot(data["poison_pcts"], data["normal_entropy"], marker='o', label=f"Ratio {ratio_key}")
    ax2.plot(data["poison_pcts"], data["poisoned_entropy"], marker='o', label=f"Ratio {ratio_key}")

ax1.set_xlabel('Poison Percentage (%)')
ax1.set_ylabel('Entropy (bits)')
ax1.set_title('Normal Prompt Entropy vs Poison Percentage')
ax1.legend()
ax1.grid(True)

ax2.set_xlabel('Poison Percentage (%)')
ax2.set_ylabel('Entropy (bits)')
ax2.set_title('Poisoned Prompt Entropy vs Poison Percentage')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('EXP_RESULTS/entropy_plot.png', dpi=300)
print(f"Plots saved to EXP_RESULTS/entropy_plot.png")

print("All experiments completed successfully.")
