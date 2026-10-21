"""Box plot of beta hat 2 by sample size, with the true delta in red."""
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ESTIMATES_PATH = ROOT / "results" / "raw" / "estimates.pk"
DATA_PATH = ROOT / "data" / "simulated.pk"
OUT_PATH = Path(__file__).resolve().parent / "beta2_boxplot.png"

with open(ESTIMATES_PATH, "rb") as f:
    estimates = pickle.load(f)
with open(DATA_PATH, "rb") as f:
    data = pickle.load(f)

sample_sizes = sorted(data)
beta2 = [estimates[estimates[:, 0] == n, 3] for n in sample_sizes]

fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot(beta2, tick_labels=[str(n) for n in sample_sizes])

# true delta differs by n (each n has its own frozen population)
for pos, n in enumerate(sample_sizes, start=1):
    ax.hlines(data[n]["delta"], pos - 0.4, pos + 0.4, colors="red",
              linestyles="dotted", linewidth=2,
              label="True $\\delta$" if pos == 1 else None)

ax.set_xlabel("Sample size (n)")
ax.set_ylabel("$\\hat\\beta_2$")
ax.set_title("MLE coefficient on treatment by sample size")
ax.legend()
fig.tight_layout()
fig.savefig(OUT_PATH, dpi=150)
print(f"Saved {OUT_PATH}")
