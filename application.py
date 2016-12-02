from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from SaferProxyFix import SaferProxyFix
import requests, json, pyowm


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@weathrzen.cbduqvubts9j.us-east-1.rds.amazonaws.com:3306/weathrzen'
db = SQLAlchemy(application)
api = Api(application)
application.wsgi_app = SaferProxyFix(application.wsgi_app)
owm = pyowm.OWM('2614605ff0159afbd9263ae7b5636a80')  # You MUST provide a valid API key


@application.route('/')
def root():
    ip = request.remote_addr
    coords = lookupIP(ip)
    city = coords[2]
    weather = lookup_weather(coords)
    return render_template('index.html', video='/static/outVod.webm', ip=ip, city=city, weather=weather)


def lookup_weather(coords):
    obs = owm.weather_at_coords(coords[1], coords[2])
    return obs.get_weather().get_status()


def lookupIP(ip):
    data = requests.get(url='http://freegeoip.net/json/{ip}'.format(ip=ip))
    binary = data.content
    output = json.loads(binary)
    return output['longitude'], output['latitude'], output['city']


if __name__ == '__main__':
    from models import Types
    from models import Gifs
    from models import Userdata
    from models import Sounds
    application.run(host='0.0.0.0')

