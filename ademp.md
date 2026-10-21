## Aims
We are attempting to recreate the core empirical result of Freedman's 2008 paper on the bias of logistic regression for estimating log odds. Namely, we aim to show that the coefficient of the logistic regression associated with the binary treatment variable is a systematic overestimate of the true difference in log-odds between a universe where all individuals receive the treatment and one where all individuals do not.

## Data-generating Mechanism
We simulate 

## Estimands
We would like to first calculate the maximum likelihood estimate of beta as used in logistic regression. We can then use this in a plug-in estimator for the true 

## Performance Measure
We will measure the raw difference between the simulated true log-odds ratio and 
-the one estimated by the plug-in estimator
-the beta coefficient corresponding to the treatment variable