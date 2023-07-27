import pandas as pd

data_minute = pd.read_pickle("./data/AAPL_min.pickle")
data_5_minute = pd.read_pickle("./data/AAPL_5_min.pickle")

# based on AAPL_min data build a new dataset by deleting some rows within the session time
# to emulate missing of some timestamps
data_minute_with_gap = data_minute.drop(
    axis=0, labels="2023-05-31 15:54:00", inplace=False
)
data_minute_with_gap = data_minute_with_gap.drop(
    axis=0, labels="2023-05-31 15:44:00", inplace=False
)

# based on AAPL_min data build a new dataset by deleting days which are not present in AAPL_5_min
data_minute_cut = data_minute[data_minute.index <= "2023-04-25 16:00:00"]

# based on AAPL_5_min data build a new dataset by deleting most rows
# and keep two days:
#  - latest with a couple of lines
#  - previous one
# The target is to emulate the case when day consists of less rows than sessionTimeDay1
data_5_minute_short_day = data_5_minute[
    (data_5_minute.index <= "2023-04-25 09:40:00")
    & (data_5_minute.index >= "2023-04-24 09:30:00")
]

# build an empty dataset
empty_data = data_5_minute_short_day[
    (data_5_minute_short_day.index > "2023-04-25 09:40:00")
    & (data_5_minute_short_day.index < "2023-04-24 09:30:00")
]

# build dataset with one row only
one_day_data = data_5_minute_short_day[
    (data_5_minute_short_day.index < "2023-04-25 00:00:00")
]
