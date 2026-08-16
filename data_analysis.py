import os
import pandas as pd

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "weather_history.csv")

COLUMNS = [
    "DateTime", "City", "Country", "Latitude", "Longitude",
    "Temperature", "Feels Like", "Humidity", "Pressure",
    "Wind Speed", "Wind Direction", "Rainfall", "Weather",
    "Description"
]


def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)


def save_weather_data(weather):
    ensure_data_file()

    row = pd.DataFrame([{
        "DateTime": weather["timestamp"],
        "City": weather["city"],
        "Country": weather["country"],
        "Latitude": weather["latitude"],
        "Longitude": weather["longitude"],
        "Temperature": weather["temperature"],
        "Feels Like": weather["feels_like"],
        "Humidity": weather["humidity"],
        "Pressure": weather["pressure"],
        "Wind Speed": weather["wind_speed"],
        "Wind Direction": weather["wind_direction"],
        "Rainfall": weather["rainfall"],
        "Weather": weather["weather"],
        "Description": weather["description"],
    }])

    if os.path.exists(DATA_FILE):
        old = pd.read_csv(DATA_FILE)
        df = pd.concat([old, row], ignore_index=True)
    else:
        df = row

    df.to_csv(DATA_FILE, index=False)


def load_weather_data():
    ensure_data_file()

    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        return df

    df["DateTime"] = pd.to_datetime(
        df["DateTime"], dayfirst=True, errors="coerce"
    )

    numeric_columns = [
        "Latitude", "Longitude", "Temperature", "Feels Like",
        "Humidity", "Pressure", "Wind Speed",
        "Wind Direction", "Rainfall"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df.sort_values("DateTime")


def get_city_history(df, city):
    result = df[df["City"] == city].copy()
    result = result.sort_values("DateTime")
    return result


def calculate_statistics(df):
    return {
        "avg_temp": df["Temperature"].mean(),
        "max_temp": df["Temperature"].max(),
        "min_temp": df["Temperature"].min(),
        "avg_humidity": df["Humidity"].mean(),
        "max_wind": df["Wind Speed"].max(),
        "total_rain": df["Rainfall"].sum(),
    }


def clear_history():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
