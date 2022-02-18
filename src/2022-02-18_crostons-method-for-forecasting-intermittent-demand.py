# # Croston's method for forecasting intermittent demand

# Use case: when a time series has many zero values.
# This is challenging for ARIMA-type models to deal
# with.

# References:
# - [sktime docs](https://www.sktime.org/en/stable/api_reference/auto_generated/sktime.forecasting.croston.Croston.html#sktime.forecasting.croston.Croston)  # noqa
# - [Blog post](https://towardsdatascience.com/croston-forecast-model-for-intermittent-demand-360287a17f5f)  # noqa
# - [Hyndman & Athanasopoulos, "Forecasting: Principles and Practice](https://otexts.com/fpp2/counts.html)  # noqa

# Croston’s method will predict a constant value for
# all future times, so Croston’s method essentially
# provides another notion for the average value of a time series.

# The method is (equivalent to) the following:
# - Let v_0 to v_n be the non-zero values of the time series
# - Let v be the exponentially smoothed average of v_0 to v_n
# - Let z_0 to z_n be the number of consecutive zeros plus 1 between the
# in the original time series.
# - Let z be the exponentially smoothed average of z_0 to z_n

# Then the forecast at a particular time is: v/z


from sktime.forecasting.croston import Croston
from sktime.datasets import load_PBS_dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"

# ## Example 1: PBS dataset

y = load_PBS_dataset()
y.tail()

forecaster = Croston(smoothing=0.1)
forecaster.fit(y)
y_pred = forecaster.predict(fh=[x for x in range(1, 11)])
y_pred.head()

# The forcaster object retains the cutoff date:

forecaster.cutoff

# Combining actuals and fitted values:

y_actual_and_fitted = pd.DataFrame(
    {"y": y, "y_fitted": forecaster._f[1:]}, index=y.index
)

y_forecast = pd.concat([y_actual_and_fitted, y_pred])
y_forecast = y_forecast.rename(columns={0: "y_predicted"})

fig, ax = plt.subplots()
y_forecast.plot(ax=ax)
ax.set_title(
    "Example 1 of forecast using Croston's method \nPharmaceutical Benefit Scheme univariate time series dataset"  # noqa
)  # noqa
fig.show()


# ## Example 2

# This is adapted from the sktime docs.

y = pd.Series([0] * 30 + [2, 2, 0, 0, 0], name="series1")

fig = plt.figure(figsize=(20, 15))
for n, smooth_value in enumerate([10, 1.5, 1, 0.5, 0.1, 0.01]):
    forecaster = Croston(smoothing=smooth_value)
    forecaster.fit(y)
    y_pred = forecaster.predict(fh=[x for x in range(1, 11)])
    y_pred.head()

    ax = plt.subplot(6, 1, n + 1)
    y.plot(ax=ax)
    y_pred.plot(ax=ax)
    ax.set_title(
        f"Example 2 of forecast using Croston's method \nAlpha = {smooth_value}"  # noqa
    )
    # ax.set_ylim(0, 10)
fig.tight_layout()
fig.show()
# fig.savefig('alpha-values.pdf')


# ## Example 3

# This is a slight modification of Example 2, with fewer zero values.

y = pd.Series(
    [0] * 10
    + np.random.choice(a=[0, 1, 2], size=35, p=[0.5, 0.1, 0.4]).tolist()
    + [2, 2, 0, 0, 0],
    name="series1",
)

fig = plt.figure(figsize=(20, 15))
for n, smooth_value in enumerate([10, 1.5, 1, 0.5, 0.1, 0.01]):
    forecaster = Croston(smoothing=smooth_value)
    forecaster.fit(y)
    y_pred = forecaster.predict(fh=[x for x in range(1, 11)])
    y_pred.head()

    ax = plt.subplot(6, 1, n + 1)
    y.plot(ax=ax)
    y_pred.plot(ax=ax)
    ax.set_title(
        f"Example 2 of forecast using Croston's method \nAlpha = {smooth_value}"  # noqa
    )
    # ax.set_ylim(0, 10)
fig.tight_layout()
fig.show()
# fig.savefig('alpha-values2.pdf')
