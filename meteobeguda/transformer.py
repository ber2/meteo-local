import datetime as dt
from dataclasses import dataclass

import pandas as pd


def only_one_day(df: pd.DataFrame, date: dt.date = dt.date.today()) -> pd.DataFrame:
    mask = df["timestamp"].dt.date == date
    return df[mask].copy()



