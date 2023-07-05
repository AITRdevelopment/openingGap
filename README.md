# openingGap

## poetry

install poetry using pip

```
poetry install
poetry shell
poetry add <PACKET>
```

## pre-commit

In .pre-commit-config.yaml we define all linters and code checkers for our code-base.
to install run:
```
($ pre-commit clean)
$ pre-commit install
$ pre-commit install-hooks
```
to run on all current files
```
pre-commit run --all-files
```
## For testing:
from root directory
```
python -m pytest 
-s to show prints in tests
--verbose to show more info

python -m pytest --cov=app/core 
```

## explanation
The real gap is two boolean values. We have a real gap up, and a real gap down. As inferred to go from one to the other the steps should be inverted.

A real gap is calculated by taking the high and low of a day ( day 0 ) and comparing that to the first x bars of day 1.
If the High of day 0 is lower than the Low of day 1, we have an opening gap up.
If the low of day 0 is higher than the high of day 1, we have an opening gap down.

The variables:
For day 0 we want to be able to select either the full day of data or the last X bars of that day. We want X to be set by using time, so '1D' should use all the data of day 0, but '1H' should only look at the last hour of candles.
For day 1 we want to be able to select the first X candles by using the same time window, so '10m' will use the first 10 minutes of candles.

Example 1 openingsGap up is True:
day 0 - high = 100 | low = 90
day 1, first 10 minutes - high = 110, low = 101

Example 2 no openingsGap:
day 0 - high = 100 | low = 90
day 1, first 10 minutes - high = 110, low = 99

Example 3 openingsGap down is True:
day 0 - high = 100 | low = 90
day 1, first 10 minutes - high = 89, low = 80

Expected input
We expect a function `openingsGap(data, sessionTimeDay0='1D', sessionTimeDay1='10m')`, that has as input a dataframe and two session times, as explained above the Day0 time window takes candles from last to first, and day1 time window takes from first to last. My tip would be to resample to '1 minutes' and calculate the amount of bars you need from there, as the market opens at 9:30 and closes at 16:00.

Expected output
We expect a dataframe with two columns: openingsGapUp and openingsGapDown with an boolean value. In the rows we expect the day datetime where the day is the day1.
