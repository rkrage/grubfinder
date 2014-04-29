import math
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import func

db = SQLAlchemy()

class FoodTruck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    facility_type = db.Column(db.String(20))
    address = db.Column(db.String(200))
    food_items = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    schedule = db.Column(db.String(200))

    def __init__(self, name, facility_type, address, food_items, latitude, longitude, schedule):
        self.name = name
        self.facility_type = facility_type
        self.address = address
        self.food_items = food_items
        self.latitude = latitude
        self.longitude = longitude
        self.schedule = schedule

    # from http://stackoverflow.com/a/11884806
    def as_dict(self):
      return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # calculate distance (in km) between food truck and geolocation
    # adapted from http://www.movable-type.co.uk/scripts/latlong.html
    @hybrid_method
    def distance(self, latitude, longitude):
        earth_radius = 6371
        dlat = math.radians(latitude - self.latitude)
        dlon = math.radians(longitude - self.longitude)
        lat1 = math.radians(self.latitude)
        lat2 = math.radians(latitude)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.sin(dlon/2) * math.sin(dlon/2) * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return earth_radius * c

    # converted distance function for use in SQL query
    @distance.expression
    def distance(cls, latitude, longitude):
        earth_radius = 6371
        pi_converter = func.pi() / 180
        dlat = (latitude - cls.latitude) * pi_converter
        dlon = (longitude - cls.longitude) * pi_converter
        lat1 = (cls.latitude) * pi_converter
        lat2 = (latitude) * pi_converter
        a = func.sin(dlat/2) * func.sin(dlat/2) + func.sin(dlon/2) * func.sin(dlon/2) * func.cos(lat1) * func.cos(lat2)
        c = 2 * func.atan2(func.sqrt(a), func.sqrt(1-a))
        return earth_radius * c
