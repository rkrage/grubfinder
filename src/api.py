import os
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
api = Api(app)
from models import FoodTruck

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
        super(FoodTruckListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        latitude = args['latitude']
        longitude = args['longitude']
        if latitude is None or longitude is None:
            query = FoodTruck.query.all()
        else:
            query = FoodTruck.query.order_by(FoodTruck.distance(latitude,longitude)).limit(10)
        result = []
        for truck in query:
            result.append(truck.as_dict())
        return result
        

api.add_resource(FoodTruckAPI, '/api/foodtrucks/<int:id>', endpoint = 'foodtruck')
api.add_resource(FoodTruckListAPI, '/api/foodtrucks', endpoint = 'foodtrucks')

if __name__ == '__main__':
    app.config['DEBUG'] = true
    app.run()
