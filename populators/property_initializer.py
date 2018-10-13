from model import Property, Partnership, Neighborhoods
from database import db
from datetime import  datetime

class PropertyInitializer():
    def init_neighborhoods(self):
        rows = []
        if not Neighborhoods.query.filter_by(name='Centro').first():
            rows.append(Neighborhoods(name='Centro', city='Cordoba'))
        if not Neighborhoods.query.filter_by(name='Cerro de las Rosas').first():
            rows.append(Neighborhoods(name='Cerro de las Rosas', city='Cordoba'))
        if not Neighborhoods.query.filter_by(name='Alberdi').first():
            rows.append(Neighborhoods(name='Alberdi', city='Cordoba'))
        if not Neighborhoods.query.filter_by(name='Jardin').first():
            rows.append(Neighborhoods(name='Jardin', city='Cordoba'))
        if not Neighborhoods.query.filter_by(name='San Martin').first():
            rows.append(Neighborhoods(name='Arguello', city='Cordoba'))

        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def init_partnership(self):
        rows = []
        if not Partnership.query.first():
            date_created = datetime.now()
            rows.append(Partnership(name='Torre Angela', address='27 de Abril 370', id_neighborhood='1',
                                    id_user='1', date_created=date_created))
            rows.append(Partnership(name='Torres de Alvear', address='Av Emilio Olmos 185', id_neighborhood='1',
                                    id_user='5', date_created=date_created))
            rows.append(Partnership(name='Lomas de la Carolina', address='Av Ej Argentin 9520', id_neighborhood='5',
                                    id_user='5', date_created=date_created))

        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    def init_properties(self):
        rows = []
        if not Property.query.first():
            date_created = datetime.now()
            rows.append(Property(id_partnership='1', floor='0', ph='A', block='', lot='')) #Id 1
            rows.append(Property(id_partnership='1', floor='0', ph='B', block='', lot=''))
            rows.append(Property(id_partnership='1', floor='0', ph='C', block='', lot=''))
            rows.append(Property(id_partnership='1', floor='1', ph='A', block='', lot=''))
            rows.append(Property(id_partnership='1', floor='1', ph='B', block='', lot=''))
            rows.append(Property(id_partnership='1', floor='1', ph='C', block='', lot=''))
            rows.append(Property(id_partnership='1', floor='1', ph='D', block='', lot=''))
            rows.append(Property(id_partnership='2', floor='0', ph='A', block='', lot='')) #Id 8
            rows.append(Property(id_partnership='2', floor='1', ph='A', block='', lot=''))
            rows.append(Property(id_partnership='2', floor='1', ph='B', block='', lot=''))
            rows.append(Property(id_partnership='2', floor='2', ph='A', block='', lot=''))
            rows.append(Property(id_partnership='2', floor='2', ph='B', block='', lot=''))
            rows.append(Property(id_partnership='2', floor='3', ph='A', block='', lot=''))
            rows.append(Property(id_partnership='2', floor='3', ph='B', block='', lot=''))
            rows.append(Property(id_partnership='3', floor='', ph='', block='8', lot='81')) #Id 15
            rows.append(Property(id_partnership='3', floor='', ph='', block='8', lot='82'))
            rows.append(Property(id_partnership='3', floor='', ph='', block='8', lot='83'))
            rows.append(Property(id_partnership='3', floor='', ph='', block='10', lot='107'))
            rows.append(Property(id_partnership='3', floor='', ph='', block='10', lot='108'))
            rows.append(Property(id_partnership='3', floor='', ph='', block='10', lot='109'))


        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e