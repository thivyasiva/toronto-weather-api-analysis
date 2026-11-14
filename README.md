# Toronto Weather API Analysis

Solo project by Thivya Siva — Toronto Metropolitan University, Bachelor of Commerce, Business Technology Management (minor in Computer Science), expected April 2027.

A Python / pandas project that fetches Toronto weather from the **Open-Meteo public API**, cleans it with pandas, stores it in **SQLite**, and exports a **Power BI-ready CSV**.

## What it does

`weather.py`:

1. Fetches hourly weather for Toronto (latitude 43.65, longitude -79.38) from Open-Meteo — no API key required.
2. Cleans the data with pandas: parses timestamps, converts types, handles missing values, adds a `date` column and a temperature band.
3. Stores the cleaned data in SQLite (`toronto_weather.db`, table `hourly_weather`).
4. Exports a Power BI-ready CSV (`toronto_weather_powerbi.csv`) with clean column names and types.
5. Prints a short summary: date range, average / minimum / maximum temperature, total precipitation.

## Skills

Python, pandas, REST API (Open-Meteo), SQLite, data cleaning, CSV export for Power BI.

## How to run

```bash
pip install -r requirements.txt
python3 weather.py
```

Options:

```bash
# Fetch the last 7 days (default) — change with --days
python3 weather.py --days 14

# Use a different output database / CSV
python3 weather.py --db my_weather.db --csv my_weather.csv
```

The script uses the Open-Meteo archive API for past days, so it works for any recent date range without a key.

## Power BI

Load `toronto_weather_powerbi.csv` into Power BI Desktop (Get Data → Text/CSV). Suggested visuals: average temperature by day (line chart), total precipitation by day (bar chart), temperature range by day, and a KPI card for average temperature.

## Files

| File | Description |
| --- | --- |
| `weather.py` | Fetch, clean, store and export script |
| `requirements.txt` | Python dependencies (pandas, requests) |
