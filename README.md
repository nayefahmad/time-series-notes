# time-series-notes
Notes on time series and forecasting methods 

## Repo structure 

- `src` directory: code files 
- `.pre-commit-config.yaml`: config for use with `pre-commit`. It specifies what hooks to use. 
  Once this file is created, if you run `pre-commit install`, the pre-commit tool will populate the 
  `pre-commit` file in the `./.git/hooks` directory. Helpful references: 
    - [Automate Python workflow using pre-commits: black and flake8](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/)
    - [Keep your code clean using Black & Pylint & Git Hooks & Pre-commit](https://towardsdatascience.com/keep-your-code-clean-using-black-pylint-git-hooks-pre-commit-baf6991f7376)
    - [pre-commit docs](https://pre-commit.com/#)
- `requirements.txt`: python packages used 

## Contents 
1. [Generating date ranges in pandas](https://github.com/nayefahmad/time-series-notes/blob/main/src/2022-01-16_generating-date-ranges.ipynb)   
2. [Croston's method for forecasting intermittent demand](https://github.com/nayefahmad/time-series-notes/blob/main/src/2022-02-18_crostons-method-for-forecasting-intermittent-demand.ipynb)
3. [Demonstrating that t-tests should not be used for time series data](https://github.com/nayefahmad/time-series-notes/blob/main/src/2022-03-04_inadequacy-of-t-tests-for-time-series-data.md)
4. [Modeling autocorrelations: Newey-West HAC and ARIMA models](https://github.com/nayefahmad/time-series-notes/blob/main/src/2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors.md)
