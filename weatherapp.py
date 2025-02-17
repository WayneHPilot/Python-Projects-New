import tkinter as tk
from tkinter import messagebox
import requests
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from datetime import datetime
import sys

load_dotenv()

# Visual Crossing API Key (Replace with your own key)
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Global variable to keep track of the canvas widget
canvas = None

# Function to convert Fahrenheit to Celsius
def fahrenheit_to_celsius(f_temp):
    return round((f_temp - 32) * 5/9, 2)

# Update the get_weather function to fetch forecast data in a separate thread
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    # Disable the button while fetching data
    btn_get_weather.config(state="disabled")
    
    # Run the fetch_data function in a separate thread to avoid freezing the GUI
    threading.Thread(target=fetch_data, args=(city,)).start()

def fetch_data(city):
    try:
        # Visual Crossing API URL for hourly forecast data
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next24hours?key={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            # Lists to hold time and temperature data
            times = []
            temps = []

            for entry in data["days"][0]["hours"]:
                raw_time = entry["datetime"]  # Extract time
                try:
                    # Try parsing the full format first (if it includes a date)
                    time = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
                except ValueError:
                    # If that fails, assume the format is just "HH:MM:SS"
                    time = datetime.strptime(raw_time, "%H:%M:%S").strftime("%H:%M")
                
                times.append(time)  # Append formatted time
                temps.append(fahrenheit_to_celsius(entry["temp"]))  # Convert temperature

            # Schedule the plot update to run in the main thread
            root.after(0, plot_temperature, times, temps)
            
            # Show the current weather info as well
            current_weather = data["currentConditions"]
            temp = fahrenheit_to_celsius(current_weather["temp"])
            weather = current_weather["conditions"]
            humidity = current_weather["humidity"]
            wind_speed = current_weather["windspeed"]
            
            weather_info = (
                f"\U0001F321 Temperature: {temp}°C\n"
                f"\u2601 Condition: {weather}\n"
                f"\U0001F4A7 Humidity: {humidity}%\n"
                f"\U0001F32C Wind Speed: {wind_speed} km/h"
            )
            weather_label.config(text=weather_info)

        else:
            messagebox.showerror("Error", "City not found. Please try again.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    # Re-enable the button after fetching data
    btn_get_weather.config(state="normal")

# Function to Plot Temperature Graph with Multiple Points
def plot_temperature(times, temps):
    global canvas  # Reference the global canvas variable
    
    # Clear previous plot by removing any existing canvas widget
    if canvas:
        canvas.get_tk_widget().destroy()

    # Ensure we have valid data
    if not times or not temps:
        messagebox.showwarning("Data Error", "No data available to plot.")
        return

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 5))  # Increase figure size for better visibility
    ax.plot(times, temps, marker="o", color="blue", label="Temperature (°C)")
    ax.set_title("Temperature Over Time (Next 24 Hours)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()

    # Rotate the time labels for better readability and reduce clutter
    plt.xticks(rotation=45, ha="right")
    ax.set_xticks(times[::2])  # Show every second time entry to widen spacing
    ax.set_xticklabels(times[::2])

    # Display the plot on the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tkinter canvas widget to display the plot
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

# Create Tkinter Window
root = tk.Tk()
root.title("\U0001F326 Live Weather App")
root.geometry("700x700")  # Increase window size for better view

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

# Function to properly close the application
def on_close():
    global root
    root.quit()  # Stop the main Tkinter loop
    root.destroy()  # Destroy the window
    sys.exit(0)  # Force exit the script

# Bind the close function to the window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Start Tkinter Main Loop
root.mainloop()
