import requests


def get_weather_for_city(city: str, api_key: str = None) -> dict:
    """
    Return: {'description': str, 'temp_c': float}
    Uses OpenWeatherMap API.
    """
    if api_key is None:
        raise ValueError("OpenWeather API key is required (set it in data/config.json)")

    base = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(base, params=params, timeout=10)
    resp.raise_for_status()
    j = resp.json()

    description = j.get("weather", [{}])[0].get("description", "No data")
    temp_c = j.get("main", {}).get("temp")
    return {"description": description, "temp_c": temp_c}
