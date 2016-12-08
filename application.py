import json
import pyowm
import requests
from flask import Flask, request, render_template
from flask_restful import Api
from application.models import Types
from application.models import Gifs
from application.models import Userdata
from application.models import Zips
from application import db
from SaferProxyFix import SaferProxyFix
from application.forms import ZipSearchForm
import datetime
import random


application = Flask(__name__)
api = Api(application)
application.wsgi_app = SaferProxyFix(application.wsgi_app)
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
owm = pyowm.OWM('2614605ff0159afbd9263ae7b5636a80')  # You MUST provide a valid API key


@application.route('/', methods=('GET', 'POST'))
def root():
    return load_main_view()


def load_main_view():
    unit = 'F'
    f_class = "active"
    c_class = ""
    cookie = request.cookies.get('unit')
    if cookie == 'celsius':
        unit = 'C'
        f_class = ""
        c_class = "active"
    zip_form = ZipSearchForm()
    ip = request.remote_addr
    coords = lookupIP(ip)
    zip_code = None
    if not zip_form.validate_on_submit():
        print zip_form.errors
    else:
        zip_code = zip_form.data
        dbcoords = convert_zip(zip_form.data)
        if dbcoords is None:
            pass
        else:
            coords = dbcoords

    city = coords[2]
    weather = lookup_weather(coords, cookie)
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
    elif weather[0].lower() == 'drizzle':
        wtype = 'rain'
    elif weather[0].lower() == 'clear':
        wtype = 'sun'
    else:
        wtype = weather[0]
    vid_url = get_vid_url(wtype.lower())
    default = vid_url[0] == ''
    # store user data in db
    store_user_data(vid_url[1], coords[0], coords[1], ip)
    timezone = get_timezone(zip_code)
    if zip_code is None:
        zip_code = -1
        return render_template('index.html', timezone=zip_code, video=vid_url[0], default=default, ip=ip, city=city,
                               weather=weather[2].title(), temp=int(round(float(weather[1]))),
                               form=zip_form, unit=unit, f_class=f_class, c_class=c_class, humidity=weather[3],
                               pressure=weather[4]['press'])
    else:
        return render_template('index.html', timezone=timezone, video=vid_url[0], default=default, ip=ip, city=city,
                            weather=weather[2].title(), temp=int(round(float(weather[1]))),
                            form=zip_form, unit=unit, f_class=f_class, c_class=c_class, humidity=weather[3], pressure=weather[4]['press'])


def get_vid_url(wtype):
    print wtype
    wid = Types.query.filter_by(type=wtype).all()[0].wid
    try:
        url = random.choice(Gifs.query.filter_by(wid=wid).all()).url
    except:
        url = ''

    return url, wid


def get_timezone(zipcode):
    try:
        return Zips.query.filter_by(zip=zipcode).all()[0].timezone
    except:
        return None


def store_user_data(wid, long, lat, ip):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = Userdata(ip=ip, datetime=date, wid=wid, longitude=long, latitude=lat)
    try:
        db.session.merge(data)
        db.session.commit()
    except:
        db.session.rollback()


def lookup_weather(coords, unit=None):
    print owm._api._cache.size()
    print owm._api._cache._table
    if unit is None:
        unit = 'fahrenheit'
    try:
        obs = owm.weather_at_coords(float(coords[1]), float(coords[0]))
    except AssertionError:
        return 'error', 'error'
    return obs.get_weather().get_status(), obs.get_weather().get_temperature(unit)['temp'],\
           obs.get_weather().get_detailed_status(), obs.get_weather().get_humidity(), obs.get_weather().get_pressure()


def lookupIP(ip):
    # ip = '64.149.143.15'
    data = requests.get(url='http://freegeoip.net/json/{ip}'.format(ip=ip))
    binary = data.content
    output = json.loads(binary)
    return output['longitude'], output['latitude'], output['city']


def convert_zip(zip):
    try:
        item=random.choice(Zips.query.filter_by(zip=zip['zip']).all())
        coords = item.longitude, item.latitude, item.city
        return coords
    except:
        return None

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True, threaded=True)

