# Hardcoded weather data for several cities
weather_data = {
    "London": {"temperature": "15°C", "conditions": "Cloudy", "wind_speed": "5 km/h", "humidity": "80%"},
    "New York": {"temperature": "20°C", "conditions": "Sunny", "wind_speed": "10 km/h", "humidity": "50%"},
    "Tokyo": {"temperature": "18°C", "conditions": "Rainy", "wind_speed": "7 km/h", "humidity": "90%"},
    "Sydney": {"temperature": "22°C", "conditions": "Windy", "wind_speed": "15 km/h", "humidity": "60%"},
    "Paris": {"temperature": "17°C", "conditions": "Foggy", "wind_speed": "3 km/h", "humidity": "85%"}
}

# Function to display weather information for a city
def display_weather(city, data):
    print(f"\nWeather forecast for {city}: ")
    print(f"Temperature: {data['temperature']}")
    print(f"Conditions: {data['conditions']}")
    print(f"Wind Speed: {data['wind_speed']}")
    print(f"Humidity: {data['humidity']}\n")

# Function to handle user input and fetch the weather data
def get_weather_forecast():
    print("Welcome to the Weather Forecast Application!\n")

    while True:
        city = input("Enter the name of the city you want the weather forecast for: ").strip()

        if city in weather_data:
            display_weather(city, weather_data[city])
            break
        else:
            print("⚠️ Invalid city name. Please enter a valid city from the list.\n")
            print("Valid cities are:", ", ".join(weather_data.keys()))

    print("Thank you for using the weather forecast application!")

# Main function to run the program
def main():
    get_weather_forecast()

if __name__ == "__main__":
    main()