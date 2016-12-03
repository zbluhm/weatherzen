from flask import Flask
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)
application.config['SQLALCHEMY_POOL_RECYCLE'] = 280
application.config['SQLALCHEMY_POOL_TIMEOUT'] = 100
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@weathrzen.cbduqvubts9j.us-east-1.rds.amazonaws.com:3306/weathrzen'
db = SQLAlchemy(application)
