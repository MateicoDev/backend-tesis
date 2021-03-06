from database import db


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.String(200), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[id_user], cascade="merge")
