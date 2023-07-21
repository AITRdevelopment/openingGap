def test_example():
    assert True


# def test_failing_example():
#    assert False


import pandas as pd

from main import df, openings_gap_inds


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
