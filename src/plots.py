"""Plots for the weather report."""

from pathlib import Path

import matplotlib.pyplot as plt


def save_figure(fig, file_name):
    """Save a figure as a PNG file, creating the folder if needed.

    Parameters:
        fig: the matplotlib figure to save
        file_name: path of the PNG file, e.g. 'figures/plot.png' (str)
    """
    Path(file_name).parent.mkdir(exist_ok=True)
    fig.savefig(file_name, dpi=150, bbox_inches="tight")


def plot_anomalies(summary, save_as=None):
    """Plot the temperature anomaly of every city over the years.

    A 10-year rolling mean is drawn instead of the raw yearly values,
    because it makes the long-term trend easier to see.

    Parameters:
        summary: yearly table with an 'anomaly' column (DataFrame)
        save_as: optional path of a PNG file where the plot is saved (str)

    Returns:
        The matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    for city in summary["city"].unique():
        city_data = summary[summary["city"] == city]
        smooth = city_data["anomaly"].rolling(10, center=True).mean()
        ax.plot(city_data["year"], smooth, label=city)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Temperature anomaly (10-year rolling mean)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Anomaly vs 1961-1990 (°C)")
    ax.legend()

    if save_as:
        save_figure(fig, save_as)
    return fig


def plot_monthly_heatmap(data, city, save_as=None):
    """Plot a heatmap of the monthly mean temperature of a city.

    Parameters:
        data: the cleaned daily table (DataFrame)
        city: name of the city to plot (str)
        save_as: optional path of a PNG file where the plot is saved (str)

    Returns:
        The matplotlib figure.
    """
    city_data = data[data["city"] == city]
    table = city_data.pivot_table(
        index="month", columns="year", values="temp_mean", aggfunc="mean"
    )

    first_year = table.columns.min()
    last_year = table.columns.max()

    fig, ax = plt.subplots(figsize=(12, 5))
    image = ax.imshow(
        table,
        aspect="auto",
        cmap="coolwarm",
        extent=[first_year, last_year + 1, 12.5, 0.5],
    )

    ax.set_yticks(range(1, 13))
    ax.set_title(f"Monthly mean temperature in {city}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Month")
    fig.colorbar(image, ax=ax, label="Mean temperature (°C)")

    if save_as:
        save_figure(fig, save_as)
    return fig


def plot_hot_days(hot_days, save_as=None):
    """Plot the average number of hot days per year in each decade.

    Parameters:
        hot_days: table returned by count_hot_days (DataFrame)
        save_as: optional path of a PNG file where the plot is saved (str)

    Returns:
        The matplotlib figure.
    """
    table = hot_days.copy()
    table["decade"] = table["year"] // 10 * 10

    average = table.pivot_table(
        index="decade", columns="city", values="hot_days", aggfunc="mean"
    )

    ax = average.plot(kind="bar", figsize=(10, 5))
    ax.set_title("Hot days per year (maximum temperature above 30 °C)")
    ax.set_xlabel("Decade")
    ax.set_ylabel("Average number of days per year")
    ax.tick_params(axis="x", rotation=0)

    fig = ax.get_figure()
    if save_as:
        save_figure(fig, save_as)
    return fig