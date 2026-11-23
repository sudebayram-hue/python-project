"""Load, clean and summarise the weather data."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")


def load_weather_data(data_dir=DATA_DIR):
    """Read all city CSV files from the data folder into one table.

    Parameters:
        data_dir: folder that contains the CSV files (Path)

    Returns:
        A pandas DataFrame with the rows of all cities.
    """
    files = sorted(Path(data_dir).glob("*.csv"))
    if not files:
        raise FileNotFoundError(
            "No CSV files found in the data folder. "
            "Run 'python src/data_loader.py' first."
        )

    tables = [pd.read_csv(file) for file in files]
    return pd.concat(tables, ignore_index=True)


def clean_weather_data(data):
    """Rename columns, convert dates and remove days without temperature.

    Parameters:
        data: the raw table returned by load_weather_data (DataFrame)

    Returns:
        A cleaned DataFrame with extra 'year' and 'month' columns.
    """
    data = data.rename(columns={
        "time": "date",
        "temperature_2m_mean": "temp_mean",
        "temperature_2m_max": "temp_max",
        "temperature_2m_min": "temp_min",
        "precipitation_sum": "precipitation",
    })

    data["date"] = pd.to_datetime(data["date"])
    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.month

    # Days without a mean temperature cannot be used in the analysis
    return data.dropna(subset=["temp_mean"])


def yearly_summary(data):
    """Compute the mean temperature and total rain for each city and year.

    Parameters:
        data: the cleaned table returned by clean_weather_data (DataFrame)

    Returns:
        A DataFrame with one row per city and year.
    """
    return data.groupby(["city", "year"]).agg(
        temp_mean=("temp_mean", "mean"),
        precipitation=("precipitation", "sum"),
    ).reset_index()