from model import RelationPropertyPerUser
from database import db

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
