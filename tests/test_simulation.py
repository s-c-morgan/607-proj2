import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dgps import make_population  # noqa: E402
from simulation import estimate, simulate_data  # noqa: E402

SIZES = [50, 100]
N_SIMS = 5


def _assert_data_equal(a, b):
    assert a.keys() == b.keys()
    for n in a:
        for key in a[n]:
            np.testing.assert_array_equal(a[n][key], b[n][key])


def test_same_seed_gives_identical_data():
    a = simulate_data(sample_sizes=SIZES, n_sims=N_SIMS, seed=123)
    b = simulate_data(sample_sizes=SIZES, n_sims=N_SIMS, seed=123)
    _assert_data_equal(a, b)


def test_different_seeds_give_different_data():
    a = simulate_data(sample_sizes=SIZES, n_sims=N_SIMS, seed=123)
    b = simulate_data(sample_sizes=SIZES, n_sims=N_SIMS, seed=456)
    assert not np.array_equal(a[100]["Z"], b[100]["Z"])


def test_same_seed_gives_identical_beta_estimates():
    a = simulate_data(sample_sizes=SIZES, n_sims=N_SIMS, seed=123)
    b = simulate_data(sample_sizes=SIZES, n_sims=N_SIMS, seed=123)
    np.testing.assert_array_equal(estimate(a), estimate(b))


def test_population_bounds():
    Z, YC, YT = make_population(10_000, rng=123)
    assert Z.min() >= 0 and Z.max() <= 1
    assert set(np.unique(YC)) <= {0, 1}
    assert set(np.unique(YT)) <= {0, 1}
