import requests
from flask import request, Flask, jsonify
from http.server import HTTPServer, BaseHTTPRequestHandler
import errorhandling as err

app = Flask(__name__)
app.config['DEBUG']=True


#API DWI
def get_weathers(city):
    #returning the weather in a specific city by inputing the name of the city
    try:
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

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET' :
        data = get_weathers(request.args.get('city'))
        weather_city = request.args.get('city')
        weather_country = data['sys']['country']
        weather_main = data['weather'][0]['main']
        weather_desc = data['weather'][0]['description']
        weather_temp = data['main']['temp']
        weather_wind = data['wind']['speed']
        res = {
            'city': weather_city,
            'country': weather_country,
            'main': weather_main,
            'desc': weather_desc,
            'temperature': weather_temp,
            'wind speed': weather_wind
        }
        return jsonify(res)

#API HATTA
def search_place(key,query):
    
    url_search ="https://maps.googleapis.com/maps/api/place/textsearch/json"
    search = {"key":key,"query":query}
    search_req = requests.get(url_search,params=search)
    print("status code search:",search_req.status_code)

    search_json = search_req.json()
        
    err.error_handling(search_json["status"])
    place_id = search_json["results"][0]["place_id"]
    return  place_id


def search_details(key,place_id):
        
    url_detail = "https://maps.googleapis.com/maps/api/place/details/json"
    details = {"key":key,"place_id":place_id}
    detail_req = requests.get(url_detail,params=details)

    print("status code details:",detail_req.status_code)
    detail_json = detail_req.json()
    err.error_handling(detail_json["status"])

    return detail_json
    

def searchapi(key,query,param='search'):
    try: 
        place_id= search_place(key,query)
        details= search_details(key,place_id)
        if param=='search':
            return details
        
        elif param=='url':
            return details["result"]["url"]
        
        elif param=='address':
            return details["result"]["adr_address"]

        elif param=='geometry':
            return details["result"]["geometry"]
    except err.ZeroResultError as e:
        message = {'results':
        {
            'status_code':404,
            'status':e.status,
            'message':e.msg,
        }, 'html_attributions':[]
        }
        return message

    except err.OverQueryError as e:
        message = {'results':
        {
            'status_code':429,
            'status':e.status,
            'message':e.msg,
        }, 'html_attributions':[]
        }
        return message

    except err.RequestDeniedError as e:
        message = {'results':
        {
            'status_code':401,
            'status':e.status,
            'message':e.msg,
        }, 'html_attributions':[]
        }
        return message

    except err.InvalidRequestError as e:
        message = {'results':
        {
            'status_code':400,
            'status':e.status,
            'message':e.msg,
        }, 'html_attributions':[]
        }
        return message
    
    except err.UnknownError as e:
        message = {'results':
        {
            'status_code':400,
            'status':e.status,
            'message':e.msg,
        }, 'html_attributions':[]
        }
        return message

    except err.NotFoundError as e:
        message = {'results':
        {
            'status_code':404,
            'status':e.status,
            'message':e.msg,
        }, 'html_attributions':[]
        }
        return message

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
    server_addr=("",1234)
    httpd = HTTPServer(server_addr, DetailHandler)
    httpd.serve_forever()
    app.run()