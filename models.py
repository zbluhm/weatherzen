from application import db


class Types(db.Model):
    wid = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return '<Type %r>' % self.type


class Userdata(db.Model):
    ip = db.Column(db.String(39), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)
    longitude = db.Column(db.Float)
    latitude = db.column(db.Float)
    wid = db.column(db.Integer, db.ForeignKey('types.wid'))

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
