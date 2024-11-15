import matplotlib.pyplot as plt
import pandas as pd
from neuralforecast import NeuralForecast
from neuralforecast.models import TimeLLM
from neuralforecast.utils import AirPassengersPanel, augment_calendar_df

AirPassengersPanel, calendar_cols = augment_calendar_df(df=AirPassengersPanel, freq="M")

Y_train_df = AirPassengersPanel[
    AirPassengersPanel.ds < AirPassengersPanel["ds"].values[-12]
]  # 132 train
Y_test_df = AirPassengersPanel[
    AirPassengersPanel.ds >= AirPassengersPanel["ds"].values[-12]
].reset_index(
    drop=True
)  # 12 test

prompt_prefix = (
    "The dataset contains data on monthly air passengers. There is a yearly seasonality"
)

timellm = TimeLLM(
    h=12,
    input_size=36,
    llm="openai-community/gpt2",
    prompt_prefix=prompt_prefix,
    batch_size=16,
    valid_batch_size=16,
    windows_batch_size=16,
)

nf = NeuralForecast(models=[timellm], freq="M")

nf.fit(df=Y_train_df, val_size=12)
forecasts = nf.predict(futr_df=Y_test_df)

Y_hat_df = forecasts.reset_index(drop=False).drop(columns=["unique_id", "ds"])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])


airline = "Airline2"

plt.plot(plot_df["ds"], plot_df["y"], c="black", label="True")
plt.plot(plot_df["ds"], plot_df["TimeLLM"], c="blue", label="median")
plt.title(f"Airline: {airline}")
plt.grid()
plt.legend()
plt.plot()
plt.show()
