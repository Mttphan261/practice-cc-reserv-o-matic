#!/usr/bin/env python3

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite://{os.path.join(BASE_DIR, 'instance/app.db')}"
# )

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, Customer, Location, Reservation
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "instance/app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def home():
    return "This is the home page"

class Customers(Resource):
    def get(self):
        customers = [c.to_dict(only=('id', 'name', 'email')) for c in Customer.query.all()]
        return make_response(customers, 200)

api.add_resource(Customers, '/customers')

class CustomerByID(Resource):
    def get(self, id):
        try:
            customer = Customer.query.filter_by(id=id).first().to_dict()
            return make_response(customer, 200)
        except:
            return {"error": "404: Customer not found"}, 404
        
api.add_resource(CustomerByID, '/customers/<int:id>')

class NewCustomer(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_customer = Customer(
                name=data['name'],
                email=data['email']
            )
            db.session.add(new_customer)
            db.session.commit()
            return make_response(new_customer.to_dict(), 201)
        except:
            return {"error": "400: Validation error"}, 400


api.add_resource(NewCustomer, '/customers')

class Locations(Resource):
    def get(self):
        locations = [l.to_dict(only=('id', 'name', 'max_party_size')) for l in Location.query.all()]
        return make_response(locations, 200)

api.add_resource(Locations, '/locations')        

class LocationByID(Resource):
    def delete(self, id):
        try:
            location = Location.query.filter_by(id=id).first()
            db.session.delete(location)
            db.session.commit()
            return make_response({}, 400)
        except:
            return {"error": "404: Activity not found"}, 404

api.add_resource(LocationByID, '/locations/<int:id>')

class NewReservation(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_reservation = Reservation(
                # reservation_date = data['reservation_date'],
                reservation_date=datetime.datetime.strptime(
                    data.get("reservation_date"), "%Y-%m-%d"
                ).date(),
                customer_id = data['customer_id'],
                location_id = data['location_id'],
                party_size = data['party_size'],
                party_name = data['party_name']
            )
            db.session.add(new_reservation)
            db.session.commit()
            return make_response(new_reservation.to_dict(), 201)
        except:
            return {"error": "400: Validation error"}, 400

api.add_resource(NewReservation, '/reservations')

class ReservationByID(Resource):
    def delete(self, id):
        try:
            reservation = Reservation.query.filter_by(id=id).first()
            db.session.delete(reservation)
            db.session.commit()
            return make_response({}, 400)
        except:
            return {"error": "404: Activity not found"}, 404

api.add_resource(ReservationByID, '/reservations/<int:id>')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
