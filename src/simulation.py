"""Replicate the Freedman (2008) Section 5 simulations.

Step 1 (simulate_data): for each n, the population (Z, YC, YT) is generated
once and frozen, and 1000 randomized experiments are drawn on it.
Saved to data/simulated.pk as {n: dict} with keys
    Z, YC, YT, delta (true differential log odds),
    X, Y (n_sims x n arrays: assignment and observed response per experiment)

Step 2 (estimate): the logit MLE and plug-in estimator are computed for every
experiment. Saved to results/raw/estimates.pk as a numpy array with columns
    n, simulation number, beta hat 1, beta hat 2, beta hat 3, plug-in estimate,
    true delta
"""
import pickle
from pathlib import Path

import numpy as np

from dgps import make_population, randomize
from metrics import true_delta
from methods import logit_mle, plug_in

SAMPLE_SIZES = [100, 500, 1000, 5000]
N_SIMS = 1000
SEED = 607
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "simulated.pk"
RESULTS_PATH = ROOT / "results" / "raw" / "estimates.pk"


def simulate_data(sample_sizes=SAMPLE_SIZES, n_sims=N_SIMS, seed=SEED):
    rng = np.random.default_rng(seed)
    data = {}
    for n in sample_sizes:
        Z, YC, YT = make_population(n, rng)
        X = np.empty((n_sims, n), dtype=int)
        Y = np.empty((n_sims, n), dtype=int)
        for s in range(n_sims):
            X[s], Y[s], _ = randomize(Z, YC, YT, frac_treated=0.75, rng=rng)
        data[n] = dict(Z=Z, YC=YC, YT=YT, delta=true_delta(YC, YT), X=X, Y=Y)
    return data


def estimate(data):
    rows = []
    for n, d in data.items():
        for s in range(d["X"].shape[0]):
            beta = logit_mle(d["X"][s], d["Y"][s], d["Z"])
            delta_tilde, _, _ = plug_in(beta, d["Z"])
            rows.append([n, s + 1, *beta, delta_tilde, d["delta"]])
    return np.array(rows)


def _save(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


if __name__ == "__main__":
    data = simulate_data()
    _save(data, DATA_PATH)
    print(f"Saved simulated data for n={list(data)} to {DATA_PATH}")

    with open(DATA_PATH, "rb") as f:
        results = estimate(pickle.load(f))
    _save(results, RESULTS_PATH)
    print(f"Saved {results.shape[0]} rows to {RESULTS_PATH}")
