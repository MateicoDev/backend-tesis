from database import db

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    id_partnership =  db.Column(db.Integer, db.ForeignKey('partnership.id'))
    partnership = db.relationship('Partnership', foreign_keys=[id_partnership], cascade="merge")
    date = db.Column(db.Date, nullable=False)
    hour = db.Column(db.Time, nullable=False)
    place = db.Column(db.String(30), nullable=False)

    def __init__(self, partnership=None, date=None, hour=None, place=None):
        self.id_partnership = partnership
        self.date = date
        self.hour = hour
        self.place = place

