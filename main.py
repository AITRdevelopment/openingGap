import pandas as pd


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



def openingsGap(data, sessionTimeDay0='1D', sessionTimeDay1='10m'):
    raise NotImplementedError()


if __name__ == '__main__':
    df = pd.read_pickle('./data/AAPL_min.pickle')
    print(openingsGap(df))
