# # Generating date ranges

import pandas as pd
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"

# Month and year, e.g. 'Nov-2014'

pd.date_range("2014-10-10", "2016-01-07", freq="MS").strftime("%b-%Y").tolist()

# Year and month, e.g. '2014-Nov'

pd.date_range("2014-10-10", "2016-01-07", freq="MS").strftime("%Y-%b").tolist()

# Months as strings from '01' to '12'

pd.date_range("2014-10-10", "2016-01-07", freq="MS").strftime("%m").tolist()

# Month names, e.g. 'Nov'

pd.date_range("2014-10-10", "2016-01-07", freq="MS").strftime("%b").tolist()

# Quarters, e.g. '01' to '04

pd.date_range("2014-10-10", "2016-01-07", freq="MS").quarter.tolist()


# # Example

# Generate a date range, then left join that with actual data.

# Date range:

reference_dates = (
    pd.date_range("2022-01-01", "2022-06-01", freq="MS")
    .strftime("%m-%Y")
    .to_list()  # noqa
)
reference_dates = pd.DataFrame({"dates": reference_dates})

# Actual data:

df = pd.DataFrame({"dates": ["2022-01-01", "2022-01-15", "2022-03-12"]})
df["dates"] = pd.to_datetime(df["dates"])
df.info()
df.head()

df["dates_formatted"] = df["dates"].dt.strftime("%m-%Y")
df.head()

# Join:
reference_dates.merge(
    df["dates_formatted"],
    how="left",
    left_on="dates",
    right_on="dates_formatted",  # noqa
)
