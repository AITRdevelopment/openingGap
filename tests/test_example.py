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
#############################################################################################


def test_example():
    assert True


# def test_failing_example():
#    assert False


# import numpy as np
import pandas as pd

from main import (  # AAPL_5_min_short_day,; AAPL_min_cut,; AAPL_min_w_gap,; empty_dataset,; one_day_dataset,
    df,
    openings_gap_inds,
    openingsGap,
)


def test8():
    pass


def test9():
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


def test1():
    assert set(openings_gap_inds["openingsGapUp"].isin([True, False])) == {
        True
    }, "openingsGapUp column has at least one blank value"


def test2():
    assert set(openings_gap_inds["openingsGapDown"].isin([True, False])) == {
        True
    }, "openingsGapDown column has at least one blank value"


def test3():
    openings_gap_inds["both_gaps"] = (
        openings_gap_inds["openingsGapUp"] & openings_gap_inds["openingsGapDown"]
    )
    assert (
        openings_gap_inds["both_gaps"].value_counts()[False]
        == openings_gap_inds.shape[0]
    ), "both openingsGapUp and openingsGapDown set for some day(s)"


def test4():
    assert (pd.Series(df.index).dt.date.nunique() - 1) == openings_gap_inds.shape[
        0
    ], "final table contains not exectly one day less then initial data"


def test5():
    assert (
        pd.Series(df.index).dt.date[0] == openings_gap_inds.index[0]
    ), "initial data and final table contains different dates in the upper row"


def test6():
    assert (
        pd.Series(df.index).dt.date[0] == openings_gap_inds.index[0]
    ), "initial data and final table contains different dates in the upper row (different latest dates)"


def test7():
    assert (
        pd.Series(df.index).dt.date.drop_duplicates(inplace=False).iloc[-2]
        == openings_gap_inds.index[-1]
    ), "the date after latest in the initial data is not the same as the earliest day in the final table"
