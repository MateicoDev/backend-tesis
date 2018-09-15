from database import db


class Partnership(db.Model):
    __tablename__ = "partnership"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    id_neighborhood = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'))
    neighborhood = db.relationship('Neighborhoods', foreign_keys=[id_neighborhood], cascade="merge")
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin = db.relationship('User', foreign_keys=[id_user], cascade="merge")
    date_created = db.Column(db.DateTime, nullable=False)

# id_user es el id de usuario del administrador del consorcio
# admin hace la relacion con usuario

# EJEMPLO PARA HACER RELACION DE UNO A UNO
#  id_user_reciver = db.Column(db.Integer, db.ForeignKey('users.id'))
 #   user_reciver = db.relationship('User', foreign_keys=[id_user_reciver], cascade="merge")

    def __init__(self, name=None, address=None, id_neighborhood=None, id_user=None, date_created=None):
        self.name = name
        self.address = address
        self.id_neighborhood = id_neighborhood
        self.id_user = id_user
        self.date_created = date_created

class Neighborhoods(db.Model):
    __tablename__ = "neighborhoods"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)

    def __init__(self, name=None, city=None):
        self.name = name
        self.city = city

class Property(db.Model):
    __tablename__="properties"
    id = db.Column(db.Integer, primary_key=True)
    id_partnership = db.Column(db.Integer, db.ForeignKey('partnership.id'))
    partnership = db.relationship('Partnership', foreign_keys=[id_partnership], cascade="merge")
    floor = db.Column(db.Integer, nullable=True) #ya que si es un country puede que sea por lote y no por piso y dpto
    ph = db.Column(db.String, nullable=True)
    block = db.Column(db.Integer, nullable=True)
    lot = db.Column(db.String, nullable=True)

    #Se dejan todos como posibles nulos, ya que puede ser lote o depto. Debe verificarse que si esta nulo uno, no
    #lo este el otro, en la vista.

    def __init__(self, id_partnership=None, floor=None, ph=None, block=None, lot=None):
        self.id_partnership = id_partnership
        self.floor = floor
        self.ph = ph
        self.block = block
        self.lot = lot

