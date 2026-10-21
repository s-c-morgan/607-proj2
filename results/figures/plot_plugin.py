"""Box plot of plug-in estimates by sample size, with the true delta in red."""
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ESTIMATES_PATH = ROOT / "results" / "raw" / "estimates.pk"
DATA_PATH = ROOT / "data" / "simulated.pk"
OUT_PATH = Path(__file__).resolve().parent / "plugin_boxplot.png"

with open(ESTIMATES_PATH, "rb") as f:
    estimates = pickle.load(f)
with open(DATA_PATH, "rb") as f:
    data = pickle.load(f)

sample_sizes = sorted(data)
plug_in = [estimates[estimates[:, 0] == n, 5] for n in sample_sizes]

fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot(plug_in, tick_labels=[str(n) for n in sample_sizes])

# true delta differs by n (each n has its own frozen population)
for pos, n in enumerate(sample_sizes, start=1):
    ax.hlines(data[n]["delta"], pos - 0.4, pos + 0.4, colors="red",
              linestyles="dotted", linewidth=2,
              label="True $\\delta$" if pos == 1 else None)

# average MLE coefficient on treatment (beta hat 2) from the raw results
for pos, n in enumerate(sample_sizes, start=1):
    ax.hlines(estimates[estimates[:, 0] == n, 3].mean(), pos - 0.4, pos + 0.4,
              colors="blue", linestyles="dotted", linewidth=2,
              label="Mean $\\hat\\beta_2$" if pos == 1 else None)

ax.set_xlabel("Sample size (n)")
ax.set_ylabel("Plug-in estimate of $\\delta$")
ax.set_title("Plug-in estimates by sample size")
ax.legend()
fig.tight_layout()
fig.savefig(OUT_PATH, dpi=150)
print(f"Saved {OUT_PATH}")
