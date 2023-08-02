#############################################################################################
#
#      Run this main.py and you will be asked to CHOOSE
#      dataset together with sessionTimeDay0/1 to pass to the openingsGap function.
#
#      You could run test with cmd
#           python -m pytest -s
#      or
#           python -m pytest -s --verbose          to show more info
#      but don't omit -s in any case!
#
#############################################################################################


import pandas as pd
from inputimeout import inputimeout

from openingsGap_func import openingsGap


from datasets_builder import (
    data_5_minute_short_day,
    data_minute_cut,
    data_minute_with_gap,
    empty_data,
    one_day_data,
)

try:
    choice = inputimeout(
        prompt="\n     \
        Chosse the input arguments set by typing corresponfing number. Then press Enter.\n \
        You have 1 min to make yout choice\n \
            1  - AAPL_min; no sessionTimeDay\n \
            2  - AAPL_5_min; no sessionTimeDay\n \
            3  - AAPL_min based df with the same earliest and latest datetime as for AAPL_5_min; no sessionTimeDay\n \
            4  - AAPL_min based df with several rows deleted; sessionTimeDay0='20m', sessionTimeDay1='15m'; gaps in the session\n \
            5  - AAPL_5_min; sessionTimeDay0='3h', sessionTimeDay1='23h'; day1 has less samples than sessionTimeDay1\n \
            6  - AAPL_5_min; sessionTimeDay1='4m', it's lower than the sampling rate\n \
                 Don't use for testing, use only to see the function output\n \
            7  - AAPL_5_min; sessionTimeDay0='10m', sessionTimeDay1='12m', it doesn't match with df sampling rate\n \
                 Don't use for testing, use only to see the function output\n \
            8  - empty df at the input; sessionTimeDay0='10m', sessionTimeDay1='10m'\n \
                 Don't use for testing, use only to see the function output\n \
            9  - one-day df at the input; sessionTimeDay0='10m', sessionTimeDay1='10m'\n \
                 Don't use for testing, use only to see the function output\n \
            10 - AAPL_5_min; sessionTimeDay0='25h', it's over than 24 hours\n \
                 Don't use for testing, use only to see the function output\n\n \
            Make your choice: ",
        timeout=60,
    )
except Exception:
    choice = "1"
    print("\n\nDefault choice (option 1) has been made, option 1")

if choice == "1":
    df = pd.read_pickle("./data/AAPL_min.pickle")
    openings_gap_inds, openings_gap_full_df = openingsGap(df)
elif choice == "2":
    df = pd.read_pickle("./data/AAPL_5_min.pickle")
    openings_gap_inds, openings_gap_full_df = openingsGap(df)
elif choice == "3":
    df = data_minute_cut
    openings_gap_inds, openings_gap_full_df = openingsGap(df)
elif choice == "4":
    df = data_minute_with_gap
    openings_gap_inds, openings_gap_full_df = openingsGap(
        df, sessionTimeDay0="20m", sessionTimeDay1="15m"
    )
elif choice == "5":
    df = data_5_minute_short_day
    openings_gap_inds, openings_gap_full_df = openingsGap(
        df, sessionTimeDay0="3h", sessionTimeDay1="23h"
    )
elif choice == "6":
    df = pd.read_pickle("./data/AAPL_5_min.pickle")
    openings_gap_inds, openings_gap_full_df = openingsGap(df, sessionTimeDay1="4m")
elif choice == "7":
    df = pd.read_pickle("./data/AAPL_5_min.pickle")
    openings_gap_inds, openings_gap_full_df = openingsGap(
        df, sessionTimeDay0="10m", sessionTimeDay1="12m"
    )
elif choice == "8":
    df = empty_data
    openings_gap_inds, openings_gap_full_df = openingsGap(
        df, sessionTimeDay0="10m", sessionTimeDay1="10m"
    )
elif choice == "9":
    df = one_day_data
    openings_gap_inds, openings_gap_full_df = openingsGap(
        df, sessionTimeDay0="10m", sessionTimeDay1="10m"
    )
elif choice == "10":
    df = pd.read_pickle("./data/AAPL_5_min.pickle")
    openings_gap_inds, openings_gap_full_df = openingsGap(df, sessionTimeDay0="25h")

if __name__ == "__main__":
    print("\nThe function output:\n\n", openings_gap_inds)
    print(
        "\nThe full df with final values:\n\n",
        openings_gap_full_df.sort_index(axis=0, ascending=False, inplace=False),
    )
