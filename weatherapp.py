import tkinter as tk
from tkinter import messagebox
import requests
from dotenv import load_dotenv
import os

load_dotenv() 

# OpenWeatherMap API Key (Replace with your own key)
API_KEY =  os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to Get Weather Data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_info = (
            f"🌡 Temperature: {temp}°C\n"
            f"☁ Condition: {weather}\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind_speed} m/s"
        )
        weather_label.config(text=weather_info)
    else:
        messagebox.showerror("Error", "City not found. Please try again.")

# Create Tkinter Window
root = tk.Tk()
root.title("🌦 Live Weather App")
root.geometry("350x300")

# City Entry
city_label = tk.Label(root, text="Enter City:", font=("Arial", 12))
city_label.pack(pady=5)

city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

# Get Weather Button
btn_get_weather = tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12))
btn_get_weather.pack(pady=10)

# Weather Info Label
weather_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
weather_label.pack(pady=10)

# Start Tkinter Main Loop
root.mainloop()
