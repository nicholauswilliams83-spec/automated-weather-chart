import requests
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from datetime import datetime
from zoneinfo import ZoneInfo


# -------------------------
# 1. Find Lufkin coordinates
# -------------------------

geo_url = "https://geocoding-api.open-meteo.com/v1/search"

geo_params = {
    "name": "Lufkin, TX",
    "count": 1,
    "countryCode": "US",
    "language": "en",
    "format": "json"
}

geo_response = requests.get(geo_url, params=geo_params)
geo_response.raise_for_status()

geo_data = geo_response.json()

location = geo_data["results"][0]

latitude = location["latitude"]
longitude = location["longitude"]
timezone = location["timezone"]

print(f"Location: {location['name']}, {location['admin1']}")
print(f"Coordinates: {latitude}, {longitude}")


# -------------------------
# 2. Get 7-day weather
# -------------------------

weather_url = "https://api.open-meteo.com/v1/forecast"

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_probability_max"
    ],
    "temperature_unit": "fahrenheit",
    "timezone": timezone,
    "forecast_days": 7
}

response = requests.get(weather_url, params=weather_params)
response.raise_for_status()

data = response.json()

dates = data["daily"]["time"]
highs = data["daily"]["temperature_2m_max"]
lows = data["daily"]["temperature_2m_min"]


# -------------------------
# 3. Make chart
# -------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    dates,
    highs,
    marker="o",
    label="High"
)

plt.plot(
    dates,
    lows,
    marker="o",
    label="Low"
)

plt.title("Lufkin, Texas — 7-Day Temperature Forecast")
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")

plt.xticks(rotation=45)
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "lufkin_7day_temperature.png",
    dpi=150
)

plt.close()


# -------------------------
# 4. Record update time
# -------------------------

central_time = datetime.now(
    ZoneInfo("America/Chicago")
)

with open("last_updated.txt", "w") as file:
    file.write(
        "Last automated update: "
        + central_time.strftime("%Y-%m-%d %I:%M:%S %p %Z")
    )

print("Lufkin weather chart successfully created.")
