#############################################################################################
#
#      You could CHOOSE dataset and sessionTimeDay0/1 to pas to the openingsGap function.
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


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!     To test on different datasets/files and/օr sessionTimeDay:
# !!      1) Uncomment import of additional datasets below ( "from datasets_builder import" line)
# !!      2) Uncomment selected dataset/file below
# !!      3) Uncomment selected session0 and session1 options below
# !!      4) Uncomment one of the openings_gap_inds options at the bottom of this file
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# to import some other datasets
# from datasets_builder import AAPL_5_min_short_day, AAPL_min_cut, AAPL_min_w_gap
#
dataset = pd.read_pickle("./data/AAPL_min.pickle")
# dataset = pd.read_pickle("./data/AAPL_5_min.pickle")
# dataset = AAPL_5_min_short_day
# AAPL_min_cut
# AAPL_min_w_gap
# session0 = '10m'
session0 = "1D"
# session1 = '15m'
# session1 = '12m'
# session1 = '23h'
session1 = "10m"


# if __name__ == "__main__":
#    df = pd.read_pickle("./data/AAPL_min.pickle")
#    print(openingsGap(df))


# if __name__ == "__main__":

df = dataset

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!     Uncomment one of two print lines to launch the function:
# !!     with uncomented above session0 and session1 as sessionTimeDay args
# !!     or without passing sessionTimeDay args
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
openings_gap_inds = openingsGap(df)
# openings_gap_inds = openingsGap(df, session0, session1)

print(openings_gap_inds)
