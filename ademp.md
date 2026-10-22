## Aims
We are attempting to recreate the core empirical result of Freedman's 2008 paper on the bias of logistic regression for estimating log odds. Namely, we aim to show that the coefficient of the logistic regression associated with the binary treatment variable is a systematic overestimate of the true difference in log-odds between a universe where all individuals receive the treatment and one where all individuals do not.

## Data-generating Mechanism

We simulate the potential control outcome for each individual by drawing n uniform (0,1) random varibles U and checking if U>0.5 for each individual. We simulate the potential treatment outcome for each individual by drawing an additional n uniform(0,1) random variables V and checking if U+V>0.75. We fix these potential outcome values for each individual, and assign each randomly to treatment or control. All randomness left is in the assignment. We choose n = 100, 500, 1000, 5000 and simulate 1000 times for each of these settings.

## Estimands
We would like the true difference in log-odds between a universe where all individuals receive the treatment and one where all individuals do not, here referred to as $
\delta$.

## Methods
We will use the Newton-Raphson algorithm to choose the maximal likelihood values of beta using the logistic log-likelihood, using the raw coefficient corresponding to the treatment covariate as a naive estimate. We will then use the full beta estimate in a plug-in estimator for the true difference in log-odds $\delta$ as specified in Freedman 2008.

## Performance Measure
We will measure the raw difference between the simulated true log-odds ratio difference and 
-the one estimated by the plug-in estimator
-the beta coefficient corresponding to the treatment variable as obtained by the MLE optimization procedure

We will also collect the standard deviations of this raw difference and of the two estimators themselves. We seek the estimator with lower raw difference that ideally exhibits convergence in standard deviation as sample size increases.