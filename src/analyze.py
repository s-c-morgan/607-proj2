"""Summarize raw simulation estimates by sample size.

Reads results/raw/estimates.pk and writes results/summary.csv with, for each n,
the mean and SD of beta hat 2 and of the plug-in estimate, plus the true delta
and each estimator's bias.
"""
import csv
import pickle
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
ESTIMATES_PATH = ROOT / "results" / "raw" / "estimates.pk"
SUMMARY_PATH = ROOT / "results" / "summary.csv"

COLUMNS = ["n", "true_delta", "beta2_mean", "beta2_sd", "beta2_bias",
           "plugin_mean", "plugin_sd", "plugin_bias"]


def summarize(estimates):
    rows = []
    for n in np.unique(estimates[:, 0]):
        r = estimates[estimates[:, 0] == n]
        beta2, plug, delta = r[:, 3], r[:, 5], r[0, 6]
        rows.append([int(n), delta, beta2.mean(), beta2.std(ddof=1),
                     beta2.mean() - delta, plug.mean(), plug.std(ddof=1),
                     plug.mean() - delta])
    return rows


if __name__ == "__main__":
    with open(ESTIMATES_PATH, "rb") as f:
        rows = summarize(pickle.load(f))
    with open(SUMMARY_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        writer.writerows(rows)
    print(f"Saved {SUMMARY_PATH}")
