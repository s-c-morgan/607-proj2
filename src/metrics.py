import numpy as np


def true_delta(YC, YT):
    """Differential log odds computed from the potential responses."""
    aT, aC = YT.mean(), YC.mean()
    return np.log(aT / (1 - aT)) - np.log(aC / (1 - aC))
