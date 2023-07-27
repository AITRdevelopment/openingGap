#############################################################################################
#
#     You could run test with cmd
#           python -m pytest -s
#      or
#           python -m pytest -s --verbose          to show more info
#      but don't omit -s in any case!
#
#      After starting the tests you will be asked to CHOOSE
#      dataset together with sessionTimeDay0/1 to pass to the openingsGap function.
#
#      Tests 1 to 6 tests Functions ability to detect incorrected input args and raise the relevant error.
#      These tests use build-in input args and don't depend on the option you choose.
#
#      Tests 7 to 12 are testing Function output dataframe itself and in cojunction with input dataframe.
#      These tests use the input args from the option you choose.
#
#############################################################################################


import numpy as np
import pandas as pd

from main import df, empty_data, one_day_data, openings_gap_inds, openingsGap
from openingsGap_func import session_time_treatment


def test_interpret_sessionTimeDay():
    assert session_time_treatment("18m") == np.timedelta64(
        18, "m"
    ), "sessionTimeDay arg wrong interpretation"
    assert session_time_treatment("3h") == np.timedelta64(
        3, "h"
    ), "sessionTimeDay arg wrong interpretation"
    assert session_time_treatment("1D") == np.timedelta64(
        1, "D"
    ), "sessionTimeDay arg wrong interpretation"


def test_empty_df_should_throw_error():
    try:
        openingsGap(empty_data)
    except Exception as e:
        assert (
            type(e) == ValueError and e.args[0] == "Initial dataframe is empty"
        ), "TEST Initial dataframe is empty PARTHLY PASSED - code should raise another error"
    else:
        assert (
            False
        ), "TEST Initial dataframe is empty NOT PASSED - code hasn't catch the issue"


def test_session_time_greater_than_day_should_throw_error():
    try:
        openingsGap(pd.read_pickle("./data/AAPL_5_min.pickle"), sessionTimeDay0="26h")
    except Exception as e:
        assert (
            type(e) == ValueError
            and e.args[0] == "Wrong input: sessionTimeDay0 is over than 24 hours"
        ), "TEST sessionTimeDay is over than 24 hours PARTHLY PASSED - code should raise another error"
    else:
        assert (
            False
        ), "TEST sessionTimeDay is over than 24 hours NOT PASSED - code hasn't catch the issue"


def test_one_day_only_df_should_throw_error():
    try:
        openingsGap(one_day_data)
    except Exception as e:
        assert (
            type(e) == ValueError
            and e.args[0] == "Initial dataframe consists of one day only"
        ), "TEST Initial dataframe consists of one day only PARTHLY PASSED - code should raise another error"
    else:
        assert (
            False
        ), "TEST Initial dataframe consists of one day only NOT PASSED - code hasn't catch the issue"


def test_session_time_lower_than_sampling_should_throw_error():
    try:
        openingsGap(pd.read_pickle("./data/AAPL_5_min.pickle"), sessionTimeDay1="4m")
    except Exception as e:
        assert (
            type(e) == ValueError
            and e.args[0]
            == "Wrong input: sessionTimeDay1 lower than data sampling rate"
        ), "TEST sessionTimeDay lower than data sampling rate PARTHLY PASSED - code should raise another error"
    else:
        assert (
            False
        ), "TEST sessionTimeDay lower than data sampling rate NOT PASSED - code hasn't catch the issue"


def test_session_time_unmatch_sampling_should_throw_error():
    try:
        openingsGap(
            pd.read_pickle("./data/AAPL_5_min.pickle"),
            sessionTimeDay0="48m",
            sessionTimeDay1="12m",
        )
    except Exception as e:
        assert (
            type(e) == ValueError
            and e.args[0]
            == "Wrong input: both sessionTimeDay0 and sessionTimeDay1 unmatch data sampling rate"
        ), "TEST sessionTimeDay unmatch data sampling rate PARTHLY PASSED - code should raise another error"
    else:
        assert (
            False
        ), "TEST sessionTimeDay unmatch data sampling rate NOT PASSED - code hasn't catch the issue"


def test_blank_gapUp_in_output_should_throw_error():
    assert set(openings_gap_inds["openingsGapUp"].isin([True, False])) == {
        True
    }, "openingsGapUp column has at least one blank value"


def test_blank_gapDown_in_output_should_throw_error():
    assert set(openings_gap_inds["openingsGapDown"].isin([True, False])) == {
        True
    }, "openingsGapDown column has at least one blank value"


def test_both_gapUp_and_Down_set_should_throw_error():
    openings_gap_inds["both_gaps"] = (
        openings_gap_inds["openingsGapUp"] & openings_gap_inds["openingsGapDown"]
    )
    assert (
        openings_gap_inds["both_gaps"].value_counts()[False]
        == openings_gap_inds.shape[0]
    ), "both openingsGapUp and openingsGapDown set for some day(s)"


def test_wrong_nbr_of_rows_in_output_should_throw_error():
    assert (pd.Series(df.index).dt.date.nunique() - 1) == openings_gap_inds.shape[
        0
    ], "final table contains not exectly one day less then initial data"


def test_wrong_latest_day_in_output_should_throw_error():
    assert (
        pd.Series(df.index).dt.date[0] == openings_gap_inds.index[0]
    ), "initial data and final table contains different dates in the upper row (different latest dates)"


def test_wrong_earliest_day_in_output_should_throw_error():
    assert (
        pd.Series(df.index).dt.date.drop_duplicates(inplace=False).iloc[-2]
        == openings_gap_inds.index[-1]
    ), "the date after latest in the initial data is not the same as the earliest day in the final table"
