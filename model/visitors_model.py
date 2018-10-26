from database import db
import datetime

class Visitor(db.Model):
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    dni = db.Column(db.String(12), nullable=False)
    sex = db.Column(db.String(1), nullable=False)

    def __init__(self, name=None, lastname=None, dni=None, sex=None):
        self.name = name
        self.lastname = lastname
        self.dni = dni
        self.sex = sex

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    id_partnership = db.Column(db.Integer, db.ForeignKey('partnership.id'))
    partnership = db.relationship('Partnership', foreign_keys=[id_partnership], cascade='merge')
    hour_since = db.Column(db.DateTime, nullable=False)
    hour_until = db.Column(db.DateTime, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_creator = db.relationship('User', foreign_keys=[id_user], cascade='merge')

    def __init__ (self, partnership=None, hourSince=None, hourUntil=None, userCreator=None):
        self.id_partnership = partnership
        self.hour_since = hourSince
        self.hour_until = hourUntil
        self.id_user = userCreator


class VisitorPerEvent(db.Model):
    __tablename__ = 'visitor_per_event'
    id = db.Column(db.Integer, primary_key=True)
    id_visitor = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    visitor = db.relationship('Visitor', foreign_keys=[id_visitor], cascade='merge')
    id_event = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event', foreign_keys=[id_event], cascade='merge')

    def __init__(self, visitor=None, event=None):
        self.id_visitor = visitor
        self.id_event = event
