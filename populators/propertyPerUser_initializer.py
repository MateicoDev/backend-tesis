from model import RelationPropertyPerUser, PropertyPerUser
from database import db
from datetime import datetime

class PropertyPerUserInitializer():
    def init_relation_propertyPerUser(self):
        rows = []
        if not RelationPropertyPerUser.query.filter_by(name='Inquilino').first():
            rows.append(RelationPropertyPerUser(name='Inquilino'))

        if not RelationPropertyPerUser.query.filter_by(name='Propietario').first():
            rows.append(RelationPropertyPerUser(name='Propietario'))

        if not RelationPropertyPerUser.query.filter_by(name='Administrador').first():
            rows.append(RelationPropertyPerUser(name='Administrador'))

        if not RelationPropertyPerUser.query.filter_by(name='Propietario Habitante').first():
            rows.append(RelationPropertyPerUser(name='Propietario Habitante'))

        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def init_propertyPerUser(self):
        rows = []
        if not PropertyPerUser.query.filter_by(user='2').first():
            date_created = datetime.now()
            rows.append(PropertyPerUser(user='2', property='1', relation='1', datecreated=date_created,
                                        datefinished=None))
            rows.append(PropertyPerUser(user='2', property='8', relation='2', datecreated=date_created,
                                        datefinished=None))
            rows.append(PropertyPerUser(user='3', property='9', relation='4', datecreated=date_created,
                                        datefinished=None))
            rows.append(PropertyPerUser(user='4', property='16', relation='1', datecreated=date_created,
                                        datefinished=None))
            rows.append(PropertyPerUser(user='4', property='3', relation='1', datecreated=date_created,
                                        datefinished=None))

        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e