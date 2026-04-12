from flask import Flask, render_template, request
import requests
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = genai.Client(api_key=os.getenv("API_KEY"))

def ai(city, bad_day, weather):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Give me a funny excuse/roast for me doing {bad_day} in {city} because the weather is {weather} in first person point of view"
    )
    return response.candidates[0].content.parts[0].text

def get_cordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    res = requests.get(url).json()
    location = res["results"][0]
    return location["latitude"], location["longitude"], location["name"], location["country"]

def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,weather_code,relative_humidity_2m,"
        f"apparent_temperature,wind_speed_10m,precipitation,cloud_cover"
    )
    res = requests.get(url).json()
    return res["current"]

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/roast", methods=["POST"])
def roast_page():
   city = request.form.get("city")
   bad_day = request.form.get("bad_day")

   lat, lon, city_name, country = get_cordinates(city)
   weather = get_weather(lat, lon)
   text=f"City: {city}, Bad_Day: {bad_day}, Weather: {weather}"
   text=ai(city, bad_day, weather)
   return render_template("index.html", text=text)

if __name__ == "__main__":
    app.run(5000, debug=True)