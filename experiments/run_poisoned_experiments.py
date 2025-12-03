import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# -------------------------
# PURE NUMPY JS-DIVERGENCE
# -------------------------
def js_divergence(p, q):
    """Compute Jensen-Shannon divergence with pure numpy."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)

    # Normalize
    p = p / (p.sum() + 1e-12)
    q = q / (q.sum() + 1e-12)

    m = 0.5 * (p + q)

    # KL divergence helper
    def kl(a, b):
        mask = (a > 0)
        return np.sum(a[mask] * np.log((a[mask] + 1e-12) / (b[mask] + 1e-12)))

    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


# -------------------------
# HELPERS
# -------------------------

def run_cmd(command):
    print(f"\n>>> Running: {command}\n")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {command}")


def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------
# EXPERIMENT SETTINGS
# -------------------------

POISON_LEVELS = [0.00, 0.01, 0.05, 0.10, 0.20]  # fraction of poison
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT = "/mmfs1/home/bryanshi/493S-project/"

RAW_INPUT = os.path.join(PROJECT, "input.txt")
GENERATE_POISON = os.path.join(PROJECT, "data/shakespeare_char/generate_poisoned_bracket_juliet.py")
PREPARE = os.path.join("data/shakespeare_char/prepare.py")
TRAIN = os.path.join("train.py")
SAMPLE = os.path.join(PROJECT, "sample.py")

RESULTS_DIR = os.path.join(PROJECT, "experiments/results")
os.makedirs(RESULTS_DIR, exist_ok=True)

NORMAL_PROMPT = os.path.join(PROJECT, "normal_prompt.txt")
POISONED_PROMPT = os.path.join(PROJECT, "poisoned_prompt.txt")


# -------------------------
# MAIN EXPERIMENT LOOP
# -------------------------

effectiveness_scores = []

for poison_frac in POISON_LEVELS:

    print(f"\n==============================")
    print(f" Running experiment: poison={poison_frac}")
    print(f"==============================")

    # 1. Generate poisoned dataset
    run_cmd(f"python3.9 {GENERATE_POISON} --poison_frac {poison_frac}")

    # 2. Run prepare.py to build dataset
    run_cmd(f"python3.9 {PREPARE}")

    # 3. Train the model
    out_dir = f"out-poison-{poison_frac}"
    run_cmd(f"python3.9 {TRAIN} config/train_shakespeare_small.py --out_dir={out_dir}")

    # 4. Generate outputs
    normal_out = os.path.join(out_dir, "normal_output.txt")
    poison_out = os.path.join(out_dir, "poisoned_output.txt")

    run_cmd(f"python3.9 {SAMPLE} --out_dir={out_dir} --start=\"FILE:{NORMAL_PROMPT}\" > {normal_out}")
    run_cmd(f"python3.9 {SAMPLE} --out_dir={out_dir} --start=\"FILE:{POISONED_PROMPT}\" > {poison_out}")

    # 5. Measure effectiveness (JS divergence between normal and poisoned generations)
    normal_text = read_text_file(normal_out)
    poison_text = read_text_file(poison_out)

    # Convert texts to character distributions
    def char_distribution(text):
        counts = {}
        for c in text:
            counts[c] = counts.get(c, 0) + 1
        keys = sorted(counts.keys())
        return np.array([counts[k] for k in keys])

    p = char_distribution(normal_text)
    q = char_distribution(poison_text)

    # Pad vectors to same length
    max_len = max(len(p), len(q))
    p = np.pad(p, (0, max_len - len(p)))
    q = np.pad(q, (0, max_len - len(q)))

    divergence = js_divergence(p, q)
    effectiveness_scores.append(divergence)

    # Save score
    with open(os.path.join(RESULTS_DIR, f"score_{poison_frac}.json"), "w") as f:
        json.dump({"js_divergence": float(divergence)}, f, indent=2)

# -------------------------
# PLOT RESULTS
# -------------------------

plt.figure(figsize=(8, 6))
plt.plot(POISON_LEVELS, effectiveness_scores, marker='o')
plt.xlabel("Poisoned Data Fraction")
plt.ylabel("Poisoning Effectiveness (JS Divergence)")
plt.title("Poison Fraction vs Training Poison Effectiveness")
plt.grid(True)

plt.savefig(os.path.join(RESULTS_DIR, "poison_plot.png"), dpi=200)
plt.show()

print("\nDone! Results saved in:", RESULTS_DIR)
