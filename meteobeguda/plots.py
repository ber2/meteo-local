import datetime as dt

import pandas as pd
import plotly.express as px
import streamlit as st


from .transformer import only_one_day


class Plotter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _ts_line_plot(self, y: str, y_label: str):
        labels = {"timestamp": "Data", y: y_label}
        return st.plotly_chart(px.line(self.df, x="timestamp", y=y, labels=labels))

    def temperature_line_plot(self):
        return self._ts_line_plot("temperature", "Temperatura (C)")

    def humidity_line_plot(self):
        return self._ts_line_plot("humidity", "Humitat (%)")

    def pressure_line_plot(self):
        return self._ts_line_plot("pressure", "Pressió atmosfèrica (hPa)")

    def rain_hourly_bar_plot(self, date: dt.date = dt.date.today()):
        d = only_one_day(self.df, date)
        d["hour"] = d.timestamp.dt.hour
        d_agg = d.groupby("hour").rain.agg("sum").reset_index()

        return st.plotly_chart(px.bar(d_agg, x="hour", y="rain", title=f"Pluja {date.isoformat()}", labels = {"hour": "Hora", "rain": "Pluja (mm)"}))

    def rain_daily_bar_plot(self):
        d = self.df.copy()
        d["date"] = d.timestamp.dt.date
        d_agg = d.groupby("date").rain.agg("sum").reset_index()

        return st.plotly_chart(px.bar(d_agg, x="date", y="rain", title="Pluja els darrers 7 dies", labels = {"date": "Data", "rain": "Pluja (mm)"}))
