import pickle

import pandas as pd

df = pd.read_pickle("./data/AAPL_min.pickle")
# print(openingsGap(df))


with open("./data/AAPL_min.pickle", "rb") as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data1min = pickle.load(f)

with open("./data/AAPL_5_min.pickle", "rb") as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data5min = pickle.load(f)


# based on AAPL_min data build a new dataset by deleting some rows within the session time
# to emulate missing of some timestamps
AAPL_min_w_gap = data1min.drop(axis=0, labels="2023-05-31 15:54:00", inplace=False)
AAPL_min_w_gap = AAPL_min_w_gap.drop(
    axis=0, labels="2023-05-31 15:44:00", inplace=False
)

# based on AAPL_min data build a new dataset by deleting days which are not present in AAPL_5_min
AAPL_min_cut = data1min[data1min.index <= "2023-04-25 16:00:00"]

# based on AAPL_5_min data build a new dataset by deleting most rows
# and keep two days:
#  - latest with a couple of lines
#  - previous one
# The target is to emulate the case when day consists of less rows than sessionTimeDay1
AAPL_5_min_short_day = data5min[
    (data5min.index <= "2023-04-25 09:40:00")
    & (data5min.index >= "2023-04-24 09:30:00")
]

# build an empty dataset
empty_dataset = AAPL_5_min_short_day[
    (AAPL_5_min_short_day.index > "2023-04-25 09:40:00")
    & (AAPL_5_min_short_day.index < "2023-04-24 09:30:00")
]
