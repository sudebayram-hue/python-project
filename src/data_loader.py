"""Download daily weather data from the Open-Meteo Historical Weather API."""

from pathlib import Path

import pandas as pd
import requests

API_URL = "https://archive-api.open-meteo.com/v1/archive"

# City name -> (latitude, longitude)
CITIES = {
    "Samsun": (41.29, 36.33),
    "Milan": (45.46, 9.19),
    "Istanbul": (41.01, 28.98),
}

DATA_DIR = Path("data")


def download_city(city, latitude, longitude,
                  start_date="1940-01-01", end_date="2025-12-31"):
    """Download daily weather data for one city.

    Parameters:
        city: name of the city (str)
        latitude: latitude of the city (float)
        longitude: longitude of the city (float)
        start_date: first day to download, format YYYY-MM-DD (str)
        end_date: last day to download, format YYYY-MM-DD (str)

    Returns:
        A pandas DataFrame with one row per day, or None if the download fails.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean,temperature_2m_max,"
                 "temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=60)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Could not download data for {city}: {error}")
        return None

    data = pd.DataFrame(response.json()["daily"])
    data["city"] = city
    return data


def save_all_cities():
    """Download the data of every city in CITIES and save it as CSV files.

    Cities whose CSV file already exists in the data folder are skipped.
    """
    DATA_DIR.mkdir(exist_ok=True)

    for city, (latitude, longitude) in CITIES.items():
        file_path = DATA_DIR / f"{city.lower()}.csv"

        if file_path.exists():
            print(f"{city}: file already exists, skipping")
            continue

        data = download_city(city, latitude, longitude)
        if data is not None:
            data.to_csv(file_path, index=False)
            print(f"{city}: saved {len(data)} rows to {file_path}")


if __name__ == "__main__":
    save_all_cities()
