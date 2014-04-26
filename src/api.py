import os
from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
api = restful.Api(app)
from models import FoodTruck

class FoodTruckAPI(restful.Resource):
    def get(self, id):
        truck = FoodTruck.query.filter(FoodTruck.id == id).first()
        if truck is not None:
            return truck.as_dict()
        return {}

class FoodTruckListAPI(restful.Resource):
    def get(self):
        trucks = FoodTruck.query.all()
        result = []
        for truck in trucks:
            result.append(truck.as_dict())
        return result

api.add_resource(FoodTruckAPI, '/api/foodtrucks/<int:id>', endpoint = 'foodtruck')
api.add_resource(FoodTruckListAPI, '/api/foodtrucks', endpoint = 'foodtrucks')

if __name__ == '__main__':
    app.config['DEBUG'] = true
    app.run()
