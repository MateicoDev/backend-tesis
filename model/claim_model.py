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
    id_user_sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_sender = db.relationship('User', foreign_keys=[id_user_sender], cascade='merge')
    id_user_reciver = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_reciver = db.relationship('User', foreign_keys=[id_user_reciver], cascade="merge")
    id_category = db.Column(db.Integer, db.ForeignKey('claim_type.id'))
    category = db.relationship('ClaimType', cascade='merge', backref=db.backref('category'))
    id_status = db.Column(db.Integer, db.ForeignKey('claim_status.id'))
    status = db.relationship('ClaimStatus', cascade='merge', backref=db.backref('status'))
    date = db.Column(db.DateTime, nullable=False)
    id_property = db.Column(db.Integer, nullable=True)
    id_partnership = db.Column(db.Integer, nullable=True)
    date_end_claim = db.Column(db.DateTime, nullable=True)
    subject = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=True)

    def __init__(self, title=None, subject=None, id_category=None, date=None, id_user=None
                 , id_property=None, id_partnership=None, id_status=None, picture=None):

        self.title = title
        self.subject = subject
        self.id_category = id_category
        self.date = date
        self.id_property = id_property
        self.id_partnership = id_partnership
        self.id_user = id_user
        self.id_status = id_status
        self.picture = picture


class ClaimMessages(db.Model):
    __tablename__ = 'claim_messages'
    id = db.Column(db.Integer, primary_key=True)
    id_user_sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_sender = db.relationship('User', foreign_keys=[id_user_sender], cascade='merge')
    id_user_reciver = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_reciver = db.relationship('User', foreign_keys=[id_user_reciver], cascade="merge")
    id_category = db.Column(db.Integer, db.ForeignKey('claim_type.id'))
    id_partnership = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String, nullable=True)
    seen = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    id_claim = db.Column(db.Integer, db.ForeignKey('claim.id'))
    claim = db.relationship('Claim', foreign_keys=[id_claim], cascade="merge")

    def __init__(self, id_user_sender=None, id_partnership=None, comment=None, date=None, id_claim=None):
        self.id_user_sender = id_user_sender
        self.id_partnership = id_partnership
        self.comment = comment
        self.date = date
        self.id_claim = id_claim
