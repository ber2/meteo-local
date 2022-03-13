import datetime as dt
from unittest import mock

import pytest
import pandas as pd

from meteobeguda.transformer import only_one_day, select_temperature, current_temperature


@pytest.fixture
def eight_days():
    return pd.read_parquet("tests/resources/eight_days.parquet")


@pytest.mark.parametrize(
    "date", [dt.date(2022, 3, 12) - dt.timedelta(k) for k in range(8)]
)
def test_only_one_day(date, eight_days):

    result = only_one_day(eight_days, date)
    assert result.timestamp.dt.date.nunique() == 1
    assert date in result.timestamp.dt.date.unique()


@pytest.fixture
def selected_temperature(eight_days):
    return select_temperature(eight_days)


def test_select_temperature_picks_only_temperature_and_timestamp(selected_temperature):
    expected_columns = ["timestamp", "temperature"]
    assert list(selected_temperature.columns) == expected_columns


def test_select_temperature_preserves_rows(selected_temperature, eight_days):
    expected_shape = (eight_days.shape[0], 2)
    assert selected_temperature.shape == expected_shape


@pytest.fixture
def current_temp(eight_days):
    return current_temperature(eight_days, dt.date(2022, 3, 12))


def test_current_temperature_min_max_are_ordered(current_temp):
    assert current_temp.min <= current_temp.temperature <= current_temp.max


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("temperature", 10.4),
        ("trend", pytest.approx(-1.1)),
        ("feels_like", 10.4),
        ("max", 12.7),
        ("max_time", dt.time(16,30)),
        ("min", 8.5),
        ("min_time", dt.time(9,15)),
    ]
)
def test_current_temperature_values(name, expected_value, current_temp):
    actual_value = getattr(current_temp, name)
    assert expected_value == actual_value

