from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from SaferProxyFix import SaferProxyFix
import requests, json, pyowm


application = Flask(__name__)
application.config['SQLALCHEMY_POOL_RECYCLE'] = 299
application.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
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
    if weather[0].lower() == 'haze':
        wtype = 'sun'
    elif weather[0].lower() == 'mist':
        wtype = 'fog'
    elif weather[0].lower() == 'tornado':
        wtype = 'rain'
    elif weather[0].lower() == 'storm':
        wtype = 'rain'
    elif weather[0].lower() == 'hurricane':
        wtype = 'rain'
    elif weather[0].lower() =='clear':
        wtype = 'sun'
    else:
        wtype = weather[0]
    vid_url = get_vid_url(wtype.lower())
    default = vid_url == ''
    return render_template('index.html', video=vid_url, default=default, ip=ip, city=city, weather=weather[0], temp=weather[1])


def get_vid_url(wtype):
    wid = 0
    url = ''
    print(wtype)
    for item in db.session.query(Types.wid).filter(Types.type==wtype):
        print(item)
        wid = item[0]

    for vid in db.session.query(Gifs.url).filter(Gifs.wid==wid):
        print(vid)
        url = vid[0]

    return url


def lookup_weather(coords):
    try:
        obs = owm.weather_at_coords(float(coords[1]), float(coords[0]))
    except AssertionError:
        return 'error', 'error'
    return obs.get_weather().get_status(), obs.get_weather().get_temperature('fahrenheit')['temp']


def lookupIP(ip):
    ip = '64.149.143.15'
    data = requests.get(url='http://freegeoip.net/json/{ip}'.format(ip=ip))
    binary = data.content
    output = json.loads(binary)
    return output['longitude'], output['latitude'], output['city']


if __name__ == '__main__':
    from models import Types
    from models import Gifs
    from models import Userdata
    from models import Sounds
    application.run(host='0.0.0.0', debug=True)

