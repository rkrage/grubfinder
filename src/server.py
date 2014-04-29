import os, urllib, json
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from models import db, FoodTruck

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
api = Api(app, catch_all_404s=True)
db.init_app(app)

# set up static routes for backbone.js
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/static/<path:filename>')
def backbone_files():
    return send_from_directory('static', filename)

# API endpoint to get truck given id
class FoodTruckAPI(Resource):
    def get(self, id):
        truck = FoodTruck.query.filter(FoodTruck.id == id).first()
        if truck is not None:
            return truck.as_dict()
        return {}

# API endpoint to get truck list given address or geolocation
class FoodTruckListAPI(Resource):

    # set up argument parsing
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
            latitude, longitude = self.geocode(address)
        if latitude is not None and longitude is not None:
            # get 20 trucks closest to geolocation ordered by distance (will only return trucks within 3 km)
            query = FoodTruck.query.filter(FoodTruck.distance(latitude,longitude) < 3).order_by(FoodTruck.distance(latitude,longitude)).limit(20)
        else:
            query = FoodTruck.query.all()
        for truck in query:
            result.append(truck.as_dict())
        return result

    # get geolocation from address using Google Maps API
    def geocode(self, addr):
        url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (urllib.quote(addr.replace(' ', '+')))
        try:
            data = urllib.urlopen(url).read()
            loc = json.loads(data).get("results")[0].get("geometry").get("location")  
        except (IndexError, IOError):
            return None, None
        return loc['lat'], loc['lng']
        
# add endpoints
api.add_resource(FoodTruckAPI, '/api/foodtrucks/<int:id>', endpoint = 'foodtruck')
api.add_resource(FoodTruckListAPI, '/api/foodtrucks', endpoint = 'foodtrucks')

# only gets here if server executed directly from python command
if __name__ == '__main__':
    app.debug = True
    app.run()
