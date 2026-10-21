"""Estimators from Freedman (2008): logit MLE and the plug-in estimator."""
import numpy as np


def _expit(t):
    return 1.0 / (1.0 + np.exp(-t))


def logit_mle(X, Y, Z, tol=1e-10, max_iter=100):
    """MLE (beta1, beta2, beta3) of the logit model P(Y=1) = expit(b1 + b2*X + b3*Z).

    The log-likelihood (12) is strictly concave, so Newton-Raphson
    converges to the unique maximum.
    """
    M = np.column_stack([np.ones(len(Y)), X, Z])
    beta = np.zeros(M.shape[1])
    for _ in range(max_iter):
        p = _expit(M @ beta)
        grad = M.T @ (Y - p)
        hess = (M * (p * (1 - p))[:, None]).T @ M
        step = np.linalg.solve(hess, grad)
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            break
    return beta


def plug_in(beta, Z):
    """Plug-in estimator of the differential log odds, eq. (10).

    Averages the predicted probabilities p(beta, 1, Z_i) and p(beta, 0, Z_i)
    over all subjects, then takes the difference of the log odds.
    Returns (delta_tilde, alpha_T_tilde, alpha_C_tilde).
    """
    aT = _expit(beta[0] + beta[1] + beta[2] * Z).mean()
    aC = _expit(beta[0] + beta[2] * Z).mean()
    delta = np.log(aT / (1 - aT)) - np.log(aC / (1 - aC))
    return delta, aT, aC
