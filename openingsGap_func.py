#############################################################################################
#
#   openingsGap func returns two values,
#   but the 2nd value is returned for testing purpose only; !! should be removed in prod !!
#
#############################################################################################


import numpy as np

# ------------------------------------------------------------------
#  Function to format the inputed sessionTimeDay as numpy.timedelta64


def session_time_treatment(session_time):
    session_time = np.timedelta64(int(session_time[:-1]), session_time[-1:])
    return session_time


# ------------------------------------------------------------------
#  Function to compare sessionTimeDay with 24 hours and drop the correspondent error flag(s) if applicable


def session_time_greater_than_day_flags_drop(
    day0_session_len, day1_session_len, sessionTimeDay0High, sessionTimeDay1High
):
    twenty_four_hours = np.timedelta64(24, "h")
    if day0_session_len <= twenty_four_hours:
        sessionTimeDay0High = False
    if day1_session_len <= twenty_four_hours:
        sessionTimeDay1High = False

    return sessionTimeDay0High, sessionTimeDay1High


# ------------------------------------------------------------------
#  Function to compare sessionTimeDay and data sampling rate, and drop the correspondent error flag(s) if applicable


def unmatch_of_session_time_and_data_sampling_rate_flags_drop(
    neigh_samples_diff,
    day0_session_len,
    day1_session_len,
    sessionTimeDay0Low,
    sessionTimeDay1Low,
    sessionTimeDay0_unmatch,
    sessionTimeDay1_unmatch,
):
    data_sampling_period = (
        neigh_samples_diff.min()
    )  # min timedelta between the neighbour timestamps

    if data_sampling_period <= day0_session_len:
        sessionTimeDay0Low = False
    if data_sampling_period <= day1_session_len:
        sessionTimeDay1Low = False

    if day0_session_len / data_sampling_period == int(
        day0_session_len / data_sampling_period
    ):
        sessionTimeDay0_unmatch = False
    if day1_session_len / data_sampling_period == int(
        day1_session_len / data_sampling_period
    ):
        sessionTimeDay1_unmatch = False

    return (
        sessionTimeDay0Low,
        sessionTimeDay1Low,
        sessionTimeDay0_unmatch,
        sessionTimeDay1_unmatch,
    )


# ------------------------------------------------------------------
#  openingsGap function


def openingsGap(data, sessionTimeDay0="1D", sessionTimeDay1="10m"):

    # ---------------------------------------------------------------
    # To verify the consistentcy of the function input args
    #  - Raise an error if the initial dataframe is empty
    #  - Raise an error if sessionTimeDay more than 24 hours
    #  - Raise an error if the initial dataframe is consists of one day only
    #  - Determinate the data initial sampling rate and raise an error if it and sessionTimeDay don't match

    if data.shape[0] == 0:
        raise ValueError("Initial dataframe is empty")

    day0_session_len = session_time_treatment(sessionTimeDay0)
    day1_session_len = session_time_treatment(sessionTimeDay1)

    # Errors flags initially set to True
    sessionTimeDay0High = True
    sessionTimeDay1High = True
    sessionTimeDay0Low = True
    sessionTimeDay1Low = True
    sessionTimeDay0_unmatch = True
    sessionTimeDay1_unmatch = True

    sessionTimeDay0High, sessionTimeDay1High = session_time_greater_than_day_flags_drop(
        day0_session_len, day1_session_len, sessionTimeDay0High, sessionTimeDay1High
    )

    if sessionTimeDay0High and sessionTimeDay1High:
        raise ValueError(
            "Wrong input: sessionTimeDay0 and sessionTimeDay1 are over than 24 hours"
        )
    elif sessionTimeDay0High:
        raise ValueError("Wrong input: sessionTimeDay0 is over than 24 hours")
    elif sessionTimeDay1High:
        raise ValueError("Wrong input: sessionTimeDay1 is over than 24 hours")

    datac = data.copy(deep=True)
    datac["date-time"] = datac.index

    if datac["date-time"].dt.date.max() == datac["date-time"].dt.date.min():
        raise ValueError("Initial dataframe consists of one day only")

    datac["neigh_samples_diff"] = datac["date-time"].diff(periods=-1)

    (
        sessionTimeDay0Low,
        sessionTimeDay1Low,
        sessionTimeDay0_unmatch,
        sessionTimeDay1_unmatch,
    ) = unmatch_of_session_time_and_data_sampling_rate_flags_drop(
        datac["neigh_samples_diff"],
        day0_session_len,
        day1_session_len,
        sessionTimeDay0Low,
        sessionTimeDay1Low,
        sessionTimeDay0_unmatch,
        sessionTimeDay1_unmatch,
    )

    if sessionTimeDay0Low and sessionTimeDay1Low:
        raise ValueError(
            "Wrong input: sessionTimeDay0 and sessionTimeDay1 lower than data sampling rate"
        )
    elif sessionTimeDay0Low:
        raise ValueError("Wrong input: sessionTimeDay0 lower than data sampling rate")
    elif sessionTimeDay1Low:
        raise ValueError("Wrong input: sessionTimeDay1 lower than data sampling rate")
    if sessionTimeDay0_unmatch and sessionTimeDay1_unmatch:
        raise ValueError(
            "Wrong input: both sessionTimeDay0 and sessionTimeDay1 unmatch data sampling rate"
        )
    elif sessionTimeDay0_unmatch:
        raise ValueError("Wrong input: sessionTimeDay0 and data sampling rate unmatch")
    elif sessionTimeDay1_unmatch:
        raise ValueError("Wrong input: sessionTimeDay1 and data sampling rate unmatch")

    # End of verification of the consistentcy of the function input args
    # ------------------------------------------------------------------

    datac.drop(columns=["open", "close", "volume"], axis=1, inplace=True)
    datac["date"] = datac["date-time"].dt.date

    # ---------------------------------------------------------------
    # Building hew dataframe with starting end ending time for each day

    days_start_end_time = datac.groupby(by="date", axis=0, as_index=True)[
        "date-time"
    ].agg(["max", "min"])
    days_start_end_time.rename(
        columns={"max": "day_end_time", "min": "day_start_time"}, inplace=True
    )

    # ---------------------------------------------------------------
    # Merging initial dataframe with with days end-start dataframe and
    # Calculate the timedelta between day0 end and day0 timestamps, and between day1 timestamps and day1 start

    datac = datac.merge(
        days_start_end_time, how="left", left_on="date", right_index=True
    )
    datac["delta_from_end"] = datac["day_end_time"] - datac["date-time"]
    datac["delta_from_start"] = datac["date-time"] - datac["day_start_time"]

    # ---------------------------------------------------------------
    # Calculate the highest high and lowest low per each day as day0 and as day1 within the sessionTimeDay0/1

    days0 = (
        datac[datac["delta_from_end"] < day0_session_len]
        .groupby(by="date", axis=0, as_index=True)
        .aggregate({"high": "max", "low": "min"})
    )
    days1 = (
        datac[datac["delta_from_start"] < day1_session_len]
        .groupby(by="date", axis=0, as_index=True)
        .aggregate({"high": "max", "low": "min"})
    )

    # ---------------------------------------------------------------
    # shift dataframe to get day1 and coreesponding day0 in the same row

    days0.drop(index=days0.last_valid_index(), axis=0, inplace=True)
    days1.drop(index=days1.first_valid_index(), axis=0, inplace=True)
    days0.reset_index(drop=False, inplace=True, names="date")
    days1.reset_index(drop=False, inplace=True, names="date")
    days01_w_shift = days0.merge(
        days1,
        how="outer",
        left_index=True,
        right_index=True,
        suffixes=("_day0", "_day1"),
    )

    # ---------------------------------------------------------------
    # determine openingsGaps indicators

    days01_w_shift["openingsGapUp"] = (
        days01_w_shift["high_day0"] < days01_w_shift["low_day1"]
    )
    days01_w_shift["openingsGapDown"] = (
        days01_w_shift["low_day0"] > days01_w_shift["high_day1"]
    )

    # ---------------------------------------------------------------
    # Building the final dataframe

    openingsGaps = days01_w_shift.drop(
        columns=["date_day0", "high_day0", "low_day0", "high_day1", "low_day1"],
        axis=1,
        inplace=False,
    )
    openingsGaps.set_index("date_day1", drop=True, append=False, inplace=True)
    openingsGaps.sort_index(axis=0, ascending=False, inplace=True)

    return (
        openingsGaps,
        days01_w_shift,
    )  # !! the 2nd value is returned for testing purpose only; should be removed in prod !!
