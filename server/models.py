from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import datetime

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"



    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False, unique=True)

    reservations = db.relationship('Reservation', back_populates='customer')
    locations = association_proxy('reservations', "location")

    #SERIALS
    serialize_rules = ('-reservations.customer',)

    #VALIDATIONS
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Customer name required')
        return name
    
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Customer email required')
        return email

    def _repr__(self):
        return f'<Customer {self.id}: {self.name}>'

class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"



    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    max_party_size = db.Column(db.Integer, nullable=False)

    reservations = db.relationship('Reservation', back_populates='location')
    customers = association_proxy('reservations', "customer")

    #SERIALS
    serialize_rules = ('-reservations.location',)

    #VALIDATIONS
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Location name required')
        return name
    
    @validates('max_party_size')
    def validate_max_party_size(self, key, max_party_size):
        if not max_party_size:
            raise ValueError('Max party size required')
        return max_party_size

    def _repr__(self):
        return f'<Location {self.id}: {self.name}>'

class Reservation(db.Model, SerializerMixin):
    __tablename__ = "reservations"



    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.Integer, nullable=False)
    party_size = db.Column(db.Integer)
    reservation_date = db.Column(db.Date, nullable=False)

    #ForeignKeys
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    #relationships
    customer = db.relationship('Customer', back_populates='reservations')
    location = db.relationship('Location', back_populates='reservations')

    serialize_rules = ('-customer.reservations', '-location.reservations',)

    #VALIDATIONS
    @validates('reservation_date')
    def validate_date(self,key,reservation_date):
        if not reservation_date or not isinstance(reservation_date, datetime.date):
            raise TypeError('Reservation date required')
        return reservation_date
    
    @validates('party_name')
    def validate_party_name(self,key,party_name):
        if not party_name or len(party_name) < 1:
            raise ValueError('Reservation party name requried')
        return party_name
    
    @validates('customer_id')
    def validate_customer_id(self, key, customer_id):
        if not customer_id or not isinstance(customer_id, int):
            raise ValueError('Customer ID required')
        return customer_id

    @validates('location_id')
    def validate_location_id(self, key, location_id):
        if not location_id or not isinstance(location_id, int):
            raise ValueError('Location ID required')
        return location_id


    def _repr__(self):
        return f'<Reservation {self.id}>'

    


