from database import db


class Partnership(db.Model):
    __tablename__ = "partnership"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    id_neighborhood = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin = db.relationship('User', foreign_keys=[id_user], cascade="merge")
    date_created = db.Column(db.DateTime, nullable=False)

