from sqlalchemy import Integer, String, Boolean, DateTime
from database import db


class ClaimType(db.Model):
    __tablename__ = 'claim_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)

    def __init__(self, name=None):
        self.name = name


class Claim(db.Model):
    __tablename__ = 'claim'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String, nullable=False)
    content = db.Column(String, nullable=True)
    category = db.Column(Integer, nullable=False)
    # category = db.Column(Integer, db.ForeignKey('{}.{}'.format('claim_type', 'id')))
    # type_category = db.relationship("ClaimType", backref=db.backref('type_of_category'))
    status = db.Column(Boolean, nullable=False)
    date = db.Column(DateTime, nullable=False)

    # def __init__(self, title=None, content=None, type_category=None,
    def __init__(self, title=None, content=None, category=None,
                 status=None, date=None):
        self.title = title
        self.content = content
        # self.type_category = category
        self.category = category
        self.status = status
        self.date = date
