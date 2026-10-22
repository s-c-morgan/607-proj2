# Bias of Logistic Regression for Estimating Log-Odds Differences

A Monte Carlo replication of the core empirical result in Freedman's paper on logistic regression in randomized experiments. We simulate randomized trials with a binary outcome (potential outcomes fixed, only treatment assignment random) at sample sizes n = 100, 500, 1000, 5000 with 1000 simulations each. We compare two estimators of the true difference in log-odds between "everyone treated" and "no one treated":

- the raw treatment coefficient from a logistic regression fit by Newton-Raphson, and
- Freedman's plug-in estimator built from the full coefficient vector.

## Setup

Requires Python 3 and `make`.

```bash
pip install -r requirements.txt   # numpy, matplotlib, pytest
```

On Windows, run `make` from Git Bash or WSL (or install GNU Make). Set `PYTHON=python3` if your interpreter has a different name: `make all PYTHON=python3`.

## Running the analysis

```bash
make all
```

This runs three steps in order:

1. `make simulate` generates the data, writing `data/simulated.pk`.
2. `make analyze` fits both estimators, writing `results/raw/estimates.pk` and `results/summary.csv`.
3. `make figures` writes the boxplots `results/figures/plugin_boxplot.png` and `results/figures/beta2_boxplot.png`.

Other targets: `make test` runs the pytest suite, and `make clean` removes generated outputs.

## Estimated runtime

About 5 seconds for `make all` on a typical laptop (measured at roughly 2 s for simulate + analyze and 2 s for figures).

## Key findings

The raw logistic treatment coefficient systematically overestimates the true log-odds difference. Its bias is roughly +0.15 to +0.31 and does not vanish as n grows to 5000. Freedman's plug-in estimator is essentially unbiased, with bias under 0.01 at every n, and its standard deviation shrinks as n increases.
