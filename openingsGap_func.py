import numpy as np

# import pandas as pd

# import pickle


def openingsGap(data, sessionTimeDay0="1D", sessionTimeDay1="10m"):

    # ------------------------------------------------------------------
    #  Function to format the inputed sessionTimeDay as numpy.timedelta64

    def session_time_treatment(session_time):
        session_time = np.timedelta64(int(session_time[:-1]), session_time[-1:])
        return session_time

    # ---------------------------------------------------------------
    # Raise an error if the initial dataframe is empty
    # Raise an error if sessionTimeDay more than 24 hours
    # Determinate the data initial sampling rate and raise an error if it and sessionTimeDay don't match

    if data.shape[0] == 0:
        raise ValueError("Initial dataframe is empty")

    day0_session_len = session_time_treatment(sessionTimeDay0)
    day1_session_len = session_time_treatment(sessionTimeDay1)
    twenyfourh = np.timedelta64(24, "h")

    # Errors flags initially set to True
    sessionTimeDay0_high = True
    sessionTimeDay1_high = True
    sessionTimeDay0_low = True
    sessionTimeDay1_low = True
    sessionTimeDay0_unmatch = True
    sessionTimeDay1_unmatch = True

    if day0_session_len <= twenyfourh:
        sessionTimeDay0_high = False
    if day1_session_len <= twenyfourh:
        sessionTimeDay1_high = False
    if sessionTimeDay0_high and sessionTimeDay1_high:
        raise ValueError(
            "Wrong input: sessionTimeDay0 and sessionTimeDay1 are over than 24 hours"
        )
    if sessionTimeDay0_high:
        raise ValueError("Wrong input: sessionTimeDay0 is over than 24 hours")
    if sessionTimeDay1_high:
        raise ValueError("Wrong input: sessionTimeDay1 is over than 24 hours")

    datac = data.copy(deep=True)
    datac["date-time"] = datac.index
    datac["neigh_samples_diff"] = datac["date-time"].diff(periods=-1)
    data_sampling_period = datac[
        "neigh_samples_diff"
    ].min()  # min timedelta between the neighbour timestamps

    if data_sampling_period <= day0_session_len:
        sessionTimeDay0_low = False
    if data_sampling_period <= day1_session_len:
        sessionTimeDay1_low = False
    if sessionTimeDay0_low and sessionTimeDay1_low:
        raise ValueError(
            "Wrong input: sessionTimeDay0 and sessionTimeDay1 lower than data sampling rate"
        )
    if sessionTimeDay0_low:
        raise ValueError("Wrong input: sessionTimeDay0 lower than data sampling rate")
    if sessionTimeDay1_low:
        raise ValueError("Wrong input: sessionTimeDay1 lower than data sampling rate")

    if day0_session_len / data_sampling_period == int(
        day0_session_len / data_sampling_period
    ):
        sessionTimeDay0_unmatch = False
    if day1_session_len / data_sampling_period == int(
        day1_session_len / data_sampling_period
    ):
        sessionTimeDay1_unmatch = False
    if sessionTimeDay0_unmatch and sessionTimeDay1_unmatch:
        raise ValueError(
            "Wrong input: both sessionTimeDay0 and sessionTimeDay1 unmatch data sampling rate"
        )
    if sessionTimeDay0_unmatch:
        raise ValueError("Wrong input: sessionTimeDay0 and data sampling rate unmatch")
    if sessionTimeDay1_unmatch:
        raise ValueError("Wrong input: sessionTimeDay1 and data sampling rate unmatch")

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

    return openingsGaps
