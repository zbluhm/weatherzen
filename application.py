import json
import pyowm
import requests
from flask import Flask, request, render_template
from flask_restful import Api
from application.models import Types
from application.models import Gifs
from application.models import Userdata
from application import db
from SaferProxyFix import SaferProxyFix
from application.forms import ZipSearchForm
import datetime

application = Flask(__name__)
api = Api(application)
application.wsgi_app = SaferProxyFix(application.wsgi_app)
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
owm = pyowm.OWM('2614605ff0159afbd9263ae7b5636a80')  # You MUST provide a valid API key


@application.route('/', methods=('GET', 'POST'))
def root():
    zip_form = ZipSearchForm(request.form)
    ip = request.remote_addr
    if request.method == 'POST' and zip_form.validate():
        pass
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
    default = vid_url[0] == ''
    # store user data in db
    store_user_data(vid_url[1], coords[0], coords[1], ip)
    return render_template('index.html', video=vid_url[0], default=default, ip=ip, city=city,
                           weather=weather[2].title(), temp=int(round(float(weather[1]))), form=zip_form)


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

    return url, wid


def store_user_data(wid, long, lat, ip):
    print lat
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = Userdata(ip=ip, datetime=date, wid=wid, longitude=long, latitude=lat)
    db.session.merge(data)
    db.session.commit()


def lookup_weather(coords):
    try:
        obs = owm.weather_at_coords(float(coords[1]), float(coords[0]))
    except AssertionError:
        return 'error', 'error'
    return obs.get_weather().get_status(), obs.get_weather().get_temperature('fahrenheit')['temp'], obs.get_weather().get_detailed_status()


def lookupIP(ip):
    ip = '64.149.143.15'
    data = requests.get(url='http://freegeoip.net/json/{ip}'.format(ip=ip))
    binary = data.content
    output = json.loads(binary)
    return output['longitude'], output['latitude'], output['city']


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)

