from database import db
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(300), nullable=True)
    hired_date = db.Column(db.DateTime, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(1), nullable=True)
    dni = db.Column(db.String(12), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    #id_property = db.Column(db.Integer, db.ForeignKey('properties.id'))
    #property = db.relationship('Property', foreign_keys=[id_property] ,cascade='merge')

    def __init__(self, username=None, password=None, name=None,
                 lastname=None, email=None,
                 profile_pic=None, birth_date=None,
                 sex=None, dni=None, phone=None):
        self.hired_date = datetime.datetime.now().date()
        self.username = username
        self.password = password
        self.name = name
        self.lastname = lastname
        self.active = True
        self.email = email
        self.profile_pic = profile_pic
        self.birth_date = birth_date
        self.sex = sex
        self.dni = dni
        self.phone = phone
        #self.id_property = property
