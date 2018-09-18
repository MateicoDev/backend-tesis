from database import db

class PropertyPerUser(db.Model):
    ___tablename__ = "propertyperuser"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[id_user], cascade="merge")
    id_property = db.Column(db.Integer, db.ForeignKey('properties.id'))
    property = db.relationship('Property', foreign_keys=[id_property], cascade="merge")
    id_relation = db.Column(db.Integer, db.ForeignKey('relationpropertyperuser.id'), nullable=True)
    relation = db.relationship('RelationPropertyPerUser', foreign_keys=[id_relation], cascade="merge")

    def __init__(self, user=None, property=None, relation=None):
        self.id_user = user
        self.id_property = property
        self.id_relation = relation


class RelationPropertyPerUser(db.Model):
    __tablename__ = "relationpropertyperuser"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name=None):
        self.name = name

