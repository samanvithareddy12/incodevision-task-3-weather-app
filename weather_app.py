import requests

# Convert weather codes into readable descriptions
def get_weather_description(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Severe thunderstorm with hail"
    }
    return weather_codes.get(code, "Unknown condition")


def get_weather():
    print("\n===== WEATHER APP =====")

    city = input("Enter city name: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    try:
        # Step 1: Find the city's coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url, params=geo_params, timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            print("City not found. Please check the spelling.")
            return

        place = geo_data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # Step 2: Get current weather information
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,weather_code,wind_speed_10m"
            ),
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url, params=weather_params, timeout=10
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        # Step 3: Display the weather
        print("\n----- CURRENT WEATHER -----")
        print("City:", place["name"])
        print("Country:", place.get("country", "N/A"))
        print("Temperature:", current["temperature_2m"], "°C")
        print("Feels Like:", current["apparent_temperature"], "°C")
        print("Humidity:", current["relative_humidity_2m"], "%")
        print(
            "Condition:",
            get_weather_description(current["weather_code"])
        )
        print("Wind Speed:", current["wind_speed_10m"], "km/h")
        print("Weather Time:", current["time"])
        print("---------------------------")

    except requests.exceptions.Timeout:
        print("The request timed out. Please try again.")

    except requests.exceptions.HTTPError as error:
        print("Weather API error:", error)

    except requests.exceptions.RequestException:
        print("Network error. Check your internet connection.")

    except (KeyError, IndexError, TypeError, ValueError):
        print("Could not read weather data. Please try again.")


if __name__ == "__main__":
    get_weather()