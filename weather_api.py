import requests
from datetime import datetime

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: ("Clear sky", "Clear"),
    1: ("Mainly clear", "Clear"),
    2: ("Partly cloudy", "Cloudy"),
    3: ("Overcast", "Cloudy"),
    45: ("Fog", "Fog"),
    48: ("Depositing rime fog", "Fog"),
    51: ("Light drizzle", "Drizzle"),
    53: ("Moderate drizzle", "Drizzle"),
    55: ("Dense drizzle", "Drizzle"),
    56: ("Light freezing drizzle", "Drizzle"),
    57: ("Dense freezing drizzle", "Drizzle"),
    61: ("Slight rain", "Rain"),
    63: ("Moderate rain", "Rain"),
    65: ("Heavy rain", "Rain"),
    66: ("Light freezing rain", "Rain"),
    67: ("Heavy freezing rain", "Rain"),
    71: ("Slight snow", "Snow"),
    73: ("Moderate snow", "Snow"),
    75: ("Heavy snow", "Snow"),
    77: ("Snow grains", "Snow"),
    80: ("Slight rain showers", "Rain"),
    81: ("Moderate rain showers", "Rain"),
    82: ("Violent rain showers", "Rain"),
    85: ("Slight snow showers", "Snow"),
    86: ("Heavy snow showers", "Snow"),
    95: ("Thunderstorm", "Thunderstorm"),
    96: ("Thunderstorm with slight hail", "Thunderstorm"),
    99: ("Thunderstorm with heavy hail", "Thunderstorm"),
}


def get_location(city):
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None, "City not found. Try another city name."

        place = results[0]
        return {
            "name": place["name"],
            "country": place.get("country", ""),
            "latitude": place["latitude"],
            "longitude": place["longitude"],
        }, None

    except requests.RequestException as exc:
        return None, f"Location service error: {exc}"


def get_weather(city):
    location, error = get_location(city)

    if error:
        return {"success": False, "error": error}

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "rain,weather_code,surface_pressure,wind_speed_10m,"
            "wind_direction_10m"
        ),
        "hourly": (
            "temperature_2m,relative_humidity_2m,rain,"
            "wind_speed_10m,weather_code"
        ),
        "forecast_days": 1,
        "timezone": "auto",
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        units = data.get("current_units", {})

        code = current.get("weather_code", 0)
        description, condition = WEATHER_CODES.get(
            code, ("Unknown", "Unknown")
        )

        hourly = data.get("hourly", {})
        temps = [
            x for x in hourly.get("temperature_2m", [])
            if isinstance(x, (int, float))
        ]

        min_temp = min(temps) if temps else current["temperature_2m"]
        max_temp = max(temps) if temps else current["temperature_2m"]

        return {
            "success": True,
            "data": {
                "city": location["name"],
                "country": location["country"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "temperature": current["temperature_2m"],
                "feels_like": current["apparent_temperature"],
                "min_temperature": min_temp,
                "max_temperature": max_temp,
                "humidity": current["relative_humidity_2m"],
                "pressure": current["surface_pressure"],
                "wind_speed": current["wind_speed_10m"],
                "wind_direction": current["wind_direction_10m"],
                "rainfall": current["rain"],
                "visibility": 10.0,
                "weather": condition,
                "description": description,
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "temperature_unit": units.get("temperature_2m", "°C"),
                "wind_unit": units.get("wind_speed_10m", "km/h"),
            },
        }

    except requests.RequestException as exc:
        return {"success": False, "error": f"Weather service error: {exc}"}
    except (KeyError, TypeError, ValueError) as exc:
        return {"success": False, "error": f"Unexpected weather data: {exc}"}
