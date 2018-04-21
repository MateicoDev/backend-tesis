from sqlalchemy import Integer, String, DateTime
from database import db


class ClaimType(db.Model):
    __tablename__ = 'claim_type'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=True)

    def __init__(self, name=None):
        self.name = name


class ClaimStatus(db.Model):
    __tablename__ = 'claim_status'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=True)

    def __init__(self, name=None):
        self.name = name


class Claim(db.Model):
    __tablename__ = 'claim'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String, nullable=False)
    dni_sender = db.Column(String(12), nullable=False)
    type_dni_sender = db.Column(String(50), nullable=False)
    content = db.Column(String, nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('claim_type.id'))
    category = db.relationship('ClaimType', cascade='merge', backref=db.backref('category'))
    id_status = db.Column(db.Integer, db.ForeignKey('claim_status.id'))
    status = db.relationship('ClaimStatus', cascade='merge', backref=db.backref('status'))
    date = db.Column(DateTime, nullable=False)
    id_property = db.Column(Integer, nullable=True)
    id_partnership = db.Column(Integer, nullable=True)
    date_end_claim = db.Column(DateTime, nullable=True)
    comment = db.Column(String, nullable=True)

    def __init__(self, title=None, content=None, category=None, date=None, dni_sender=None,
                 type_dni_sender=None, id_property=None, id_partnership=None, comment=None):

        self.title = title
        self.content = content
        self.category = category
        self.date = date
        self.dni_sender = dni_sender
        self.type_dni_sender = type_dni_sender
        self.id_property = id_property
        self.id_partnership = id_partnership
        self.id_status = 1
        self.comment = comment
