from model import SpendingType
from database import db


class SpendingTypeInitializer():
    def init_types_of_spending(self):
        rows = []
        if not SpendingType.query.filter_by(name='Limpieza').first():
            rows.append(SpendingType(name='Limpieza'))

        if not SpendingType.query.filter_by(name='Guardia').first():
            rows.append(SpendingType(name='Guardia'))

        if not SpendingType.query.filter_by(name='Servicios').first():
            rows.append(SpendingType(name='Servicios'))

        if not SpendingType.query.filter_by(name='Mantenimiento').first():
            rows.append(SpendingType(name='Mantenimiento'))

        if not SpendingType.query.filter_by(name='Otros').first():
            rows.append(SpendingType(name='Otros'))

        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
