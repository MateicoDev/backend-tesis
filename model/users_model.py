from database import db
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(60), nullable=False)
    user_password = db.Column(db.String(150), nullable=False)
    user_name = db.Column(db.String(45), nullable=False)
    user_lastname = db.Column(db.String(45), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    user_email = db.Column(db.String(100), nullable=False)
    user_profile_pic = db.Column(db.String(300), nullable=True)
    user_hired_date = db.Column(db.DateTime, nullable=False)
    user_birth_date = db.Column(db.DateTime, nullable=False)
    user_sex = db.Column(db.String(1), nullable=True)
    user_dni = db.Column(db.String(12), nullable=True)
    user_phone = db.Column(db.String(30), nullable=True)

    def __init__(self, user_username=None, user_password=None, user_name=None,
                 user_lastname=None, user_email=None,
                 user_profile_pic=None, user_birth_date=None,
                 user_sex=None, user_dni=None, user_phone=None):
        self.user_hired_date = datetime.datetime.now().date()
        self.user_username = user_username
        self.user_password = user_password
        self.user_name = user_name
        self.user_lastname = user_lastname
        self.active = True
        self.user_email = user_email
        self.user_profile_pic = user_profile_pic
        self.user_birth_date = user_birth_date
        self.user_sex = user_sex
        self.user_dni = user_dni
        self.user_phone = user_phone
