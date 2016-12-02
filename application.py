from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from SaferProxyFix import SaferProxyFix
import requests, json


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@weathrzen.cbduqvubts9j.us-east-1.rds.amazonaws.com:3306/weathrzen'
db = SQLAlchemy(application)
api = Api(application)
application.wsgi_app = SaferProxyFix(application.wsgi_app)


@application.route('/')
def root():
    ip = request.remote_addr
    city = lookupIP(ip)
    return render_template('index.html', video='/static/outVod.webm', out="FUck u", ip=ip, city=city)


def lookupIP(ip):

    data = requests.get(url='http://freegeoip.net/json/{ip}'.format(ip=ip))
    binary = data.content
    output = json.loads(binary)
    return output['city']


if __name__ == '__main__':
    from models import Types
    from models import Gifs
    from models import Userdata
    from models import Sounds
    application.run(host='0.0.0.0')

