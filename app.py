# import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = 'your_api_key_here'
        if not api_key:
            return "API key not set. Please set the OPENWEATHERMAP_API_KEY environment variable.", 500

        city = request.form["city"]
        if not city:
            return "Please enter a city name."

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == "404":
                return "City not found. Please check the city name and try again."

            city = data["name"]
            weather_description = data["weather"][0]["description"].capitalize()
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            icon_id = data["weather"][0]['icon']


            icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

            return render_template("index.html", city=city, weather_description=weather_description,
                                   temperature=temperature, feels_like=feels_like, humidity=humidity,
                                   wind_speed=wind_speed, icon_url=icon_url)

        except requests.RequestException as e:
            return "Error fetching weather data.", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)