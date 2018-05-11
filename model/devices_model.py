from sqlalchemy import Integer, String, ForeignKey
from database import db

class Device(db.Model):
    __tablename__ = 'devices'
    id_user_device = db.Column(Integer, primary_key=True)
    registration_id = db.Column(String(200), nullable=False)
    id_user = db.Column(Integer, ForeignKey('users.id_user'))
    user = db.relationship('User', foreign_keys=[id_user], cascade="merge")