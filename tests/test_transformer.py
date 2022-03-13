import datetime as dt

import pytest
import pandas as pd

from meteobeguda.transformer import only_one_day


@pytest.fixture
def eight_days():
    return pd.read_parquet("tests/resources/eight_days.parquet")

@pytest.mark.parametrize(
    "date",
    [dt.date(2022, 3, 12) - dt.timedelta(k)
     for k in range(8)]
)
def test_only_one_day(date, eight_days):

    result = only_one_day(eight_days, date)
    assert result.timestamp.dt.date.nunique() == 1
    assert date in result.timestamp.dt.date.unique()
