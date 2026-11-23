"""Numerical analysis of the yearly weather summary."""

import numpy as np

BASELINE_START = 1961
BASELINE_END = 1990


def add_anomalies(summary, start=BASELINE_START, end=BASELINE_END):
    """Add the temperature anomaly of each year to the summary table.

    The anomaly is the mean temperature of a year minus the average
    temperature of a reference period, computed separately for each city.

    Parameters:
        summary: yearly table returned by yearly_summary (DataFrame)
        start: first year of the reference period (int)
        end: last year of the reference period (int)

    Returns:
        A copy of the table with an extra 'anomaly' column.
    """
    summary = summary.copy()
    summary["anomaly"] = 0.0

    for city in summary["city"].unique():
        is_city = summary["city"] == city
        in_period = summary["year"].between(start, end)
        reference = summary.loc[is_city & in_period, "temp_mean"].mean()
        summary.loc[is_city, "anomaly"] = (
            summary.loc[is_city, "temp_mean"] - reference
        )

    return summary


def temperature_trend(summary, city):
    """Estimate how fast the mean temperature of a city is changing.

    A straight line is fitted to the yearly mean temperatures.

    Parameters:
        summary: yearly table returned by yearly_summary (DataFrame)
        city: name of the city (str)

    Returns:
        The temperature change in degrees Celsius per decade (float).
    """
    city_data = summary[summary["city"] == city]
    slope, intercept = np.polyfit(city_data["year"], city_data["temp_mean"], 1)
    return slope * 10

def count_hot_days(data, threshold=30):
    """Count the days per year in which the maximum temperature is hot.

    A day is 'hot' if its maximum temperature is above the threshold.

    Parameters:
        data: the cleaned daily table (DataFrame)
        threshold: temperature in degrees Celsius above which a day is hot (float)

    Returns:
        A DataFrame with one row per city and year and a 'hot_days' column.
    """
    data = data.copy()
    data["hot_days"] = np.where(data["temp_max"] > threshold, 1, 0)
    return data.groupby(["city", "year"])["hot_days"].sum().reset_index()