from database import db


class ClaimType(db.Model):
    __tablename__ = 'claim_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)

    def __init__(self, name=None):
        self.name = name


class ClaimStatus(db.Model):
    __tablename__ = 'claim_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)

    def __init__(self, name=None):
        self.name = name


class Claim(db.Model):
    __tablename__ = 'claim'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    dni_sender = db.Column(db.String(12), nullable=False)
    type_dni_sender = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('claim_type.id'))
    category = db.relationship('ClaimType', cascade='merge', backref=db.backref('category'))
    id_status = db.Column(db.Integer, db.ForeignKey('claim_status.id'))
    status = db.relationship('ClaimStatus', cascade='merge', backref=db.backref('status'))
    date = db.Column(db.DateTime, nullable=False)
    id_property = db.Column(db.Integer, nullable=True)
    id_partnership = db.Column(db.Integer, nullable=True)
    date_end_claim = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.String, nullable=True)

    def __init__(self, title=None, content=None, id_category=None, date=None, dni_sender=None,
                 type_dni_sender=None, id_property=None, id_partnership=None, id_status=None):

        self.title = title
        self.content = content
        self.id_category = id_category
        self.date = date
        self.dni_sender = dni_sender
        self.type_dni_sender = type_dni_sender
        self.id_property = id_property
        self.id_partnership = id_partnership
        self.id_status = id_status
