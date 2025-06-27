import os
import logging
from datetime import date, datetime, timedelta

import requests

from agents import Agent, function_tool

from settings import REQUEST_TIMEOUT

code_map = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog and depositing rime fog",
    48: "fog and depositing rime fog",
    51: "drizzle: light intensity",
    53: "drizzle: moderate intensity",
    55: "drizzle: dense intensity",
    56: "freezing drizzle: light intensity",
    57: "freezing drizzle: dense intensity",
    61: "rain: slight intensity",
    63: "rain: moderate intensity",
    65: "rain: heavy intensity",
    66: "freezing rain: light intensity",
    67: "freezing rain: heavy intensity",
    71: "snow fall: slight intensity",
    73: "snow fall: moderate intensity",
    75: "snow fall: heavy intensity",
    77: "snow grains",
    80: "rain showers: slight intensity",
    81: "rain showers: moderate intensity",
    82: "rain showers: violent intensity",
    85: "snow showers: slight intensity",
    86: "snow showers: heavy intensity",
    95: "thunderstorm: slight or moderate",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail"
}

@function_tool
def get_today() -> str:
    return f"Today is {date.today()}"


@function_tool
def get_coordinates(location: str) -> str:
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search"
    try:
        geo_resp = requests.get(geo_url, params={"name": location}, timeout=REQUEST_TIMEOUT)
        geo_resp.raise_for_status()
        data = geo_resp.json()
        result = data["results"][0]
        return f"{location} coordinates are {result['latitude']} latitude and {result['longitude']} longitude. This location is in {result['country']}."
    except (KeyError, IndexError):
        return f"Could not find coordinates for {location}"
    except requests.RequestException:
        return f"Error fetching data for {location}"


@function_tool
def get_days_between_dates(fromStr: str, toStr: str) -> str:
    fromDate = datetime.fromisoformat(fromStr).date()
    toDate = datetime.fromisoformat(toStr).date()
    days = (toDate - fromDate).days
    return f"The dates are {days} days apart."


@function_tool
def get_weather(latitude: str, longitude: str, target_date: str) -> str:
    """
    Returns the weather for the date provided. It can only forecast up to 6 days ahead.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        target_date: Target date
    """
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode"
    try:
        weather_resp = requests.get(weather_url, timeout=REQUEST_TIMEOUT)
        weather_resp.raise_for_status()
        data = weather_resp.json()
        if target_date in data["daily"]["time"]:
            index = data["daily"]["time"].index(target_date)
            weathercode = data["daily"]["weathercode"][index]
            if weathercode not in code_map:
                logging.warning(f"Unusual weathercode encountered: {weathercode}")
            return f"The weather at latitude {latitude} and longitude {longitude} will be {code_map.get(weathercode, "unusual conditions")}."
        else:
            return "I don't know the weather for the date provided."
    except requests.RequestException:
        return f"Error fetching weather data for coordinates {latitude}, {longitude}"


