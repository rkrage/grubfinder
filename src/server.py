import os, urllib, json
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
api = Api(app)
from models import FoodTruck

def geocode(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (urllib.quote(addr.replace(' ', '+')))
    try:
        data = urllib.urlopen(url).read()
        loc = json.loads(data).get("results")[0].get("geometry").get("location")  
    except (IndexError, IOError):
        return None, None
    return loc['lat'], loc['lng']

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/static/<path:filename>')
def backbone_files():
    return send_from_directory('static', filename)

class FoodTruckAPI(Resource):
    def get(self, id):
        truck = FoodTruck.query.filter(FoodTruck.id == id).first()
        if truck is not None:
            return truck.as_dict()
        return {}

class FoodTruckListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('latitude', type = float, required = False)
        self.reqparse.add_argument('longitude', type = float, required = False)
        self.reqparse.add_argument('address', type = str, required = False)
        super(FoodTruckListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        address = args['address']
        latitude = args['latitude']
        longitude = args['longitude']
        result = []
        if address is not None:
            latitude, longitude = geocode(address)
        if latitude is not None and longitude is not None:
            query = FoodTruck.query.filter(FoodTruck.distance(latitude,longitude) < 3).order_by(FoodTruck.distance(latitude,longitude)).limit(10)
        else:
            query = FoodTruck.query.all()
        for truck in query:
            result.append(truck.as_dict())
        return result
        

api.add_resource(FoodTruckAPI, '/api/foodtrucks/<int:id>', endpoint = 'foodtruck')
api.add_resource(FoodTruckListAPI, '/api/foodtrucks', endpoint = 'foodtrucks')


if __name__ == '__main__':
    app.run()
