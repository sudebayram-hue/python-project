# Weather Report

Is the climate really changing where we live? This project downloads daily
weather data from 1940 to 2025 for three cities (Samsun, Milan and Istanbul)
and studies how temperatures have changed over time.

Project for the Python module of the *Coding for Data Science and Data
Management* course (A.Y. 2026/27).

## What the project does

- downloads daily temperature and precipitation data from the Open-Meteo API
- cleans the data and computes yearly summaries with pandas
- computes temperature anomalies (compared with 1961-1990), the warming
  trend per decade and the number of hot days per year with numpy
- plots the anomalies, monthly temperature heatmaps and hot days with matplotlib
- presents the results in a Jupyter notebook

## Data source

[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
(free, no registration). The data is model-based reanalysis data, not direct
station measurements. The CSV files are not stored in this repository: they
are downloaded by a script (see below).

## Method

1. **Download:** daily mean, maximum and minimum temperature and total precipitation for each city (1940-2025).
2. **Cleaning:** rename the columns, convert the dates, add year and month, drop days without a mean temperature.
3. **Yearly summary:** mean temperature and total precipitation for each city and year.
4. **Anomaly:** yearly mean temperature minus the average of the reference period 1961-1990 of the same city.
5. **Trend:** a straight line is fitted to the yearly mean temperatures (`numpy.polyfit`); its slope is the warming per decade.
6. **Hot days:** number of days per year with a maximum temperature above 30 °C.

## Limitations

- The data is model-based reanalysis, not direct station measurements.
- The trend is a single straight line over 86 years, so it hides that most of the warming happened after 1990.
- Only three cities are analysed.
- The 2020s contain only six years (2020-2025).
- The 30 °C threshold for hot days is a choice; other thresholds give different numbers.

## Project structure

```
python-project/
├── src/
│   ├── data_loader.py       # downloads the data and saves it as CSV
│   ├── data_processing.py   # loads, cleans and summarises the data
│   ├── analysis.py          # anomalies, trend and hot days (numpy)
│   └── plots.py             # plotting functions (matplotlib)
├── figures/                 # saved plots
├── weather_report.ipynb     # presentation notebook
├── requirements.txt         # Python libraries
└── README.md
```

## How to run

1. Clone the repository and enter the folder:
   ```
   git clone https://github.com/sudebayram-hue/python-project.git
   cd python-project
   ```
2. Install the libraries (Python 3.14 was used):
   ```
   pip install -r requirements.txt
   ```
3. Download the data into the `data/` folder:
   ```
   python src/data_loader.py
   ```
   If the server answers "429 Too Many Requests", wait a few minutes and run
   the command again: cities that were already downloaded are skipped.
4. Open `weather_report.ipynb` (for example in VS Code) and run all the cells.

## Main results

| City     | Warming trend 1940-2025 |
|----------|-------------------------|
| Milan    | +0.31 °C per decade     |
| Samsun   | +0.17 °C per decade     |
| Istanbul | +0.13 °C per decade     |

Temperatures were stable until about 1990 and then increased quickly in all
three cities.

![Temperature anomaly](figures/anomalies.png)

Hot days (maximum temperature above 30 °C) became much more frequent: in
2011-2025 Milan has about 31 hot days per year, against about 8 in 1961-1990.

![Hot days](figures/hot_days.png)

## Libraries

pandas, numpy, matplotlib, requests (see `requirements.txt` for versions).