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

fig, ax = plt.subplots()
y.plot(ax=ax)
ax.set_title("PBS dataset")
fig.show()

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

# Here we can see that alpha values between 0 and 1.0 seem sensible.
# The larger the value of alpha, the more our fit weights recent
# data points.

y = pd.Series([0] * 30 + [2, 2, 0, 0, 0], name="series1")

fig = plt.figure(figsize=(20, 15))
for n, smooth_value in enumerate([10, 1.5, 1, 0.5, 0.1, 0.01]):
    forecaster = Croston(smoothing=smooth_value)
    forecaster.fit(y)
    y_pred = forecaster.predict(fh=[x for x in range(1, 11)])
    y_pred.head()

    df_fitted = pd.DataFrame(
        {"y": y, "y_fitted": forecaster._f[1:]}, index=y.index
    )  # noqa
    df_pred = pd.concat([df_fitted, y_pred])
    df_pred = df_pred.rename(columns={0: "y_predicted"})

    ax = plt.subplot(6, 1, n + 1)
    df_pred.plot(ax=ax)
    ax.set_title(
        f"Example 2 of forecast using Croston's method \nAlpha = {smooth_value}"  # noqa
    )
fig.tight_layout()
fig.show()
# fig.savefig('dst/alpha-values.pdf')


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

    df_fitted = pd.DataFrame(
        {"y": y, "y_fitted": forecaster._f[1:]}, index=y.index
    )  # noqa
    df_pred = pd.concat([df_fitted, y_pred])
    df_pred = df_pred.rename(columns={0: "y_predicted"})

    ax = plt.subplot(6, 1, n + 1)
    df_pred.plot(ax=ax)
    ax.set_title(
        f"Example 2 of forecast using Croston's method \nAlpha = {smooth_value}"  # noqa
    )
    # ax.set_ylim(0, 10)
fig.tight_layout()
fig.show()
# fig.savefig('dst/alpha-values2.pdf')


# ## Example 4

# Here we try to see how forecasts change as we spread out/cluster the
# positive values

y_not_clustered = pd.Series(
    [0, 1] + [0] * 3 + [1] + [0] * 3 + [1],
    name="y_not_clustered",
)

y_clustered = pd.Series(
    [0] * 7 + [1, 1, 1],
    name="y_clustered",
)

smooth_value = 0.1  # todo: try different smooth_values

fig = plt.figure(figsize=(10, 5))
for n, y_series in enumerate([y_not_clustered, y_clustered]):
    forecaster = Croston(smoothing=smooth_value)
    forecaster.fit(y_series)
    y_pred = forecaster.predict(fh=[x for x in range(1, 4)])

    df_fitted = pd.DataFrame(
        {"y": y_series, "y_fitted": forecaster._f[1:]}, index=y_series.index
    )  # noqa
    df_pred = pd.concat([df_fitted, y_pred])
    df_pred = df_pred.rename(columns={0: "y_predicted"})

    plt.suptitle("This is a suptitle", size=24, y=1.02)
    ax = plt.subplot(2, 1, n + 1)
    df_pred.plot(ax=ax)
    ax.set_title(
        f"Example 4 of forecast using Croston's method \nAlpha = {smooth_value}\n Series name = {y_series.name}"  # noqa
    )
    ax.set_ylim(0, 3)
fig.tight_layout()
fig.show()
# fig.savefig('clustered-vs-not-clustered.pdf')
