import pandas as pd

def openingsGap(data, sessionTimeDay0='1D', sessionTimeDay1='10m'):
    raise NotImplementedError()


if __name__ == '__main__':
    df = pd.read_pickle('./data/AAPL_min.pickle')
    print(openingsGap(df))
