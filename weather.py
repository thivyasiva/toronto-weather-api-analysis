"""Toronto Weather API Analysis.

Solo project. Fetches Toronto hourly weather from the Open-Meteo
public API (no key required), cleans it with pandas, stores it in
SQLite, and exports a Power BI-ready CSV.

Usage:
    python3 weather.py [--days 7] [--db toronto_weather.db]
                       [--csv toronto_weather_powerbi.csv]
"""
import argparse
import sqlite3
from datetime import date, timedelta

import pandas as pd
import requests

LATITUDE = 43.65
LONGITUDE = -79.38
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def parse_args():
    parser = argparse.ArgumentParser(description="Toronto weather API analysis")
    parser.add_argument("--days", type=int, default=7, help="Number of past days to fetch (default: 7)")
    parser.add_argument("--db", default="toronto_weather.db", help="SQLite database file (default: toronto_weather.db)")
    parser.add_argument("--csv", default="toronto_weather_powerbi.csv", help="Power BI-ready CSV output (default: toronto_weather_powerbi.csv)")
    return parser.parse_args()


def fetch_weather(days):
    end = date.today() - timedelta(days=1)  # archive API covers complete days
    start = end - timedelta(days=days - 1)
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "America/Toronto",
    }
    response = requests.get(ARCHIVE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def clean_weather(payload):
    hourly = payload["hourly"]
    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(columns={
        "time": "timestamp",
        "temperature_2m": "temperature_c",
        "relative_humidity_2m": "humidity_pct",
        "precipitation": "precipitation_mm",
        "wind_speed_10m": "wind_speed_kmh",
    })
    df["date"] = df["timestamp"].dt.date
    df = df.dropna(subset=["temperature_c"])
    df["temperature_band"] = pd.cut(
        df["temperature_c"],
        bins=[-30, 0, 10, 20, 30, 50],
        labels=["Below 0C", "0-10C", "10-20C", "20-30C", "Above 30C"],
    )
    return df


def main():
    args = parse_args()
    payload = fetch_weather(args.days)
    df = clean_weather(payload)

    with sqlite3.connect(args.db) as conn:
        df.to_sql("hourly_weather", conn, if_exists="replace", index=False)

    df.to_csv(args.csv, index=False)

    print(f"Toronto weather — {df['date'].min()} to {df['date'].max()}")
    print(f"Hours fetched: {len(df)}")
    print(f"Average temperature: {df['temperature_c'].mean():.1f} C")
    print(f"Minimum temperature: {df['temperature_c'].min():.1f} C")
    print(f"Maximum temperature: {df['temperature_c'].max():.1f} C")
    print(f"Total precipitation: {df['precipitation_mm'].sum():.1f} mm")
    print(f"Stored in SQLite: {args.db} (table hourly_weather)")
    print(f"Power BI-ready CSV: {args.csv}")


if __name__ == "__main__":
    main()
