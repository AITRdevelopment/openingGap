#############################################################################################
#
#      You could CHOOSE dataset together with sessionTimeDay0/1 to pass to the openingsGap function.
#      Please see the comments marked with !!!! below for details.
#
#############################################################################################

# import numpy as np
import pandas as pd

from openingsGap_func import openingsGap

# import pickle


"""
def resample(data, sample):
    resampled_data = (
        data.resample(sample)
        .agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }
        )
        .dropna()
    )
    resampled_data.index.name = "datetime"
    return resampled_data
"""


# def openingsGap(data, c="1D", sessionTimeDay1="10m"):
#    raise NotImplementedError()


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!
# !!    To import some other datasets, uncomment the line below
# !!    Datasets are described in datasets_builder.py
# !!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# from datasets_builder import AAPL_5_min_short_day, AAPL_min_cut, AAPL_min_w_gap, empty_dataset


# if __name__ == "__main__":
#    df = pd.read_pickle("./data/AAPL_min.pickle")
#    print(openingsGap(df))


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!
# !!     Uncomment two subsequent lines to launch the function with specified args
# !!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
df = pd.read_pickle("./data/AAPL_min.pickle")
openings_gap_inds = openingsGap(df)
#
# df = pd.read_pickle("./data/AAPL_5_min.pickle")
# openings_gap_inds = openingsGap(df)
#
# df = AAPL_min_cut
# openings_gap_inds = openingsGap(df)
#
# df = pd.read_pickle("./data/AAPL_5_min.pickle")
# openings_gap_inds = openingsGap(df, sessionTimeDay0='10m', sessionTimeDay1='4m')
#
# df = pd.read_pickle("./data/AAPL_5_min.pickle")
# openings_gap_inds = openingsGap(df, sessionTimeDay0='10m', sessionTimeDay1='12m')
#
# df = AAPL_min_w_gap
# openings_gap_inds = openingsGap(df, sessionTimeDay0='10m', sessionTimeDay1='12m')
#
# df = AAPL_5_min_short_day
# openings_gap_inds = openingsGap(df, sessionTimeDay0='3h', sessionTimeDay1='23h')
#
# df = empty_dataset
# openings_gap_inds = openingsGap(df, sessionTimeDay0='3h', sessionTimeDay1='23h')

print(openings_gap_inds)
