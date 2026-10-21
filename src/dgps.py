"""Data generator from Freedman (2008), Section 5.

Subject-level potential responses are built once and then frozen; the only
randomness in an experiment is the assignment to treatment/control.
"""
import numpy as np


def make_population(n, rng=None):
    """Return frozen covariate and potential responses (Z, YC, YT).

    U, V ~ IID Uniform(0, 1); Z = V;
    YC = 1 if U > 1/2; YT = 1 if U + V > 3/4.
    """
    rng = np.random.default_rng(rng)
    U = rng.uniform(size=n)
    V = rng.uniform(size=n)
    Z = V
    YC = (U > 0.5).astype(int)
    YT = (U + V > 0.75).astype(int)
    return Z, YC, YT


def randomize(Z, YC, YT, frac_treated=0.75, rng=None):
    """Run one randomized experiment on a frozen population.

    Exactly round(frac_treated * n) subjects are chosen at random for
    treatment (X = 1); the rest go to control (X = 0). The observed
    response is Y = X*YT + (1 - X)*YC.
    """
    rng = np.random.default_rng(rng)
    n = len(Z)
    nT = int(round(frac_treated * n))
    X = np.zeros(n, dtype=int)
    X[rng.choice(n, size=nT, replace=False)] = 1
    Y = X * YT + (1 - X) * YC
    return X, Y, Z


def true_delta(YC, YT):
    """Differential log odds computed from the potential responses."""
    aT, aC = YT.mean(), YC.mean()
    return np.log(aT / (1 - aT)) - np.log(aC / (1 - aC))
