from application import db


class Types(db.Model):
    wid = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))

    def __init__(self, wid, type):
        self.wid = wid
        self.type = type

    def __repr__(self):
        return '<Type %r>' % self.type


class Userdata(db.Model):
    ip = db.Column(db.String(39), primary_key=True)
    wid = db.Column(db.Integer, db.ForeignKey('types.wid'))
    datetime = db.Column(db.DateTime, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, ip, datetime, longitude, latitude, wid):
        self.datetime = datetime
        self.ip = ip
        self.longitude = longitude
        self.latitude = latitude
        self.wid = wid

    def __repr__(self):
        return '<Ip %r>' % self.ip


class Gifs(db.Model):
    wid = db.Column(db.Integer, db.ForeignKey('types.wid'), primary_key=True, )
    url = db.Column(db.String(100), primary_key=True)

    def __init__(self, wid, url):
        self.wid = wid
        self.url = url

    def __repr__(self):
        return '<URL %r>' % self.url


class Sounds(db.Model):
    wid = db.Column(db.Integer, db.ForeignKey('types.wid'), primary_key=True)
    url = db.Column(db.String(100), primary_key=True)

    def __init__(self, wid, url):
        self.wid = wid
        self.url = url

    def __repr__(self):
        return '<URL %r>' % self.url


class Zips(db.Model):
    zip = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(15), primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timezone = db.Column(db.Integer)

    def __init__(self, zip, city, latitude, longitude, timezone):
        self.zip = zip
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone

    def __repr__(self):
        return '<Zip %r>' % self.zip

class Zipsnew(db.Model):
    zip = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(15), primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timezone = db.Column(db.Integer)

    def __init__(self, zip, city, latitude, longitude, timezone):
        self.zip = zip
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone

    def __repr__(self):
        return '<Zip %r>' % self.zip