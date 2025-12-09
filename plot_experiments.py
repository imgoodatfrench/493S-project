import matplotlib.pyplot as plt
import json

# Load results from JSON
with open('EXP_RESULTS/entropy_results.json', 'r') as f:
    results = json.load(f)

# Create plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

for ratio_key, data in results.items():
    ax1.plot(data["poison_pcts"], data["normal_entropy"], marker='o', label=f"Ratio {ratio_key}")
    ax2.plot(data["poison_pcts"], data["poisoned_entropy"], marker='o', label=f"Ratio {ratio_key}")

ax1.set_xlabel('Code Word Percentage (%)')
ax1.set_ylabel('Entropy (bits)')
ax1.set_title('Normal Prompt Entropy vs Code Word Percentage')
ax1.legend()
ax1.grid(True)

ax2.set_xlabel('Code Word Percentage (%)')
ax2.set_ylabel('Entropy (bits)')
ax2.set_title('Poisoned Prompt Entropy vs Code Word Percentage')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('EXP_RESULTS/entropy_plot.png', dpi=300)
print(f"Plots saved to EXP_RESULTS/entropy_plot.png")

plt.show()