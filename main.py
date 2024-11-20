from datetime import timedelta, datetime
import requests
import pyttsx3
import json


def speak_and_print(message):
    print(message)
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID=6ed1776958e669a7a1271cef6ab2a5dc"
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raises an HTTPError if the response code is not 200
        weather_data = r.text  # Get the raw response text (string)
        return json.loads(weather_data)  # Parse it using the json module
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def convert_temperature(kelvin):
    """Convert temperature from Kelvin to Celsius and Fahrenheit."""
    celsius = kelvin - 273.15
    fahrenheit = (celsius * 9 / 5) + 32
    # Return the formatted string directly
    return f"{round(celsius, 2)} °C", f"{round(fahrenheit, 2)} °F"


def format_sunrise_sunset(timestamp, timezone_offset):
    """Format sunrise and sunset times from the UNIX timestamp."""
    # Convert timestamp to datetime object
    utc_time = datetime.utcfromtimestamp(timestamp)
    # Apply timezone offset (convert from UTC to local time)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%H:%M:%S")


def main():
    speak_and_print("Welcome to WeatherApp")

    while True:
        speak_and_print("Enter the Name of city (or type 'exit' to quit): ")
        city = input()
        if city.lower() == 'exit':
            speak_and_print("Goodbye!")
            break

        weather_data = get_weather_data(city)
        if weather_data is None or "error" in weather_data:
            speak_and_print("City not found. Please check the name and try again.")

        else:
            city_name = weather_data["name"]
            country_name = weather_data["sys"]["country"]
            weather_description = weather_data["weather"][0]["description"]
            temp = convert_temperature(weather_data["main"]["temp"])
            feels_like = convert_temperature(weather_data["main"]["feels_like"])
            temp_min = convert_temperature(weather_data["main"]["temp_min"])
            temp_max = convert_temperature(weather_data["main"]["temp_max"])
            pressure = weather_data["main"]["pressure"]
            humidity = weather_data["main"]["humidity"]
            visibility = weather_data["visibility"]
            wind_speed = weather_data["wind"]["speed"]
            wind_deg = weather_data["wind"]["deg"]
            cloud_cover = weather_data["clouds"]["all"]
            sunrise_time = format_sunrise_sunset(weather_data["sys"]["sunrise"], weather_data["timezone"])
            sunset_time = format_sunrise_sunset(weather_data["sys"]["sunset"], weather_data["timezone"])
            longitude = weather_data["coord"]["lon"]
            latitude = weather_data["coord"]["lat"]

            message = f"""

                   City: {city_name}, {country_name}
                   Weather: {weather_description}
                   Temperature: {temp} 
                   Feels Like: {feels_like} 
                   Min Temp: {temp_min}     Max Temp: {temp_max}  
                   Humidity: {humidity} %     Visibility: {visibility} meters
                   Pressure: {pressure} hPa 
                   Wind Speed: {wind_speed} m/s     Wind Direction: {wind_deg} degrees
                   Cloud Cover: {cloud_cover} %
                   Sunrise: {sunrise_time}am     Sunset: {sunset_time}pm
                   Longitude: {longitude}     Latitude: {latitude}
                   """
            speak_and_print(message)


if __name__ == "__main__":
    main()
