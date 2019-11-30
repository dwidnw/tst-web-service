import requests
import json
import re
import urllib.request
from flask import request, Flask, jsonify, render_template
from pytube import YouTube 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['DEBUG']=True


#API DWI
def get_weathers(city):
    #returning the weather in a specific city by inputing the name of the city
    try:
        res=[]
        param={
            'q':city,
            'appid':'3d6ae3df59815d39dbf27c8a52460ed0'
        }
        url = 'https://api.openweathermap.org/data/2.5/weather'
        res = requests.get(url, params=param)
        return res.json()
    except Exception as e:
        res = "The Weather in"+city+"Could Not Be Found"
        return res

@app.route('/weather', methods=['GET'])
def index():
    if request.method == 'GET' :
        data = get_weathers(request.args.get('city'))
        weather_city = request.args.get('city')
        weather_country = data['sys']['country']
        coord_lon = data['coord']['lon']
        coord_lat = data['coord']['lat']
        weather_main = data['weather'][0]['main']
        weather_desc = data['weather'][0]['description']
        weather_temp = data['main']['temp']
        weather_press = data['main']['pressure']
        weather_hum = data['main']['humidity']
        weather_wind = data['wind']['speed']

        res = {
            'city': weather_city,
            'country': weather_country,
            'longitude': coord_lon,
            'latitude': coord_lat,
            'main weather': weather_main,
            'description': weather_desc,
            'temperature': weather_temp,
            'pressure': weather_press,
            'humidity': weather_hum,
            'wind speed': weather_wind
        }
        return jsonify(res)

#API CLAUDIA
api_key = "AIzaSyAKkGJ78S330UDgvqQ6E04hmhCTGNygf7Q"

def youtubeSearch(keyword): 
    try : 
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&order=relevance&q="+keyword.replace(" ", "%20")+"&key="+api_key
        json_url= urllib.request.urlopen(url)
        data = json.loads(json_url.read())
        res = []
        # hasil = []
        
        for item in data['items'] : 
            result  = {
                'url' : "https://m.youtube.com/watch?v="+item['id']['videoId'],
                'title' : item['snippet']['title'], 
                'publishedAt' : item['snippet']['publishedAt']
            }
            res.append(result)
        return jsonify(res)
    except : 
        req = "Video Not Found."
        return req

@app.route('/api/ytubesearch', methods=['GET'])
def index2():
    masukkan = request.args.get('keyword')
    return youtubeSearch(masukkan)
    
# execute the app #
if __name__ == '__main__':
    app.run()
