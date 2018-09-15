from model import ClaimType, ClaimStatus
from database import db


class ClaimInitializer():
    def init_status_claims(self):
        rows = []
        if not ClaimStatus.query.filter_by(name='Creada').first():
            rows.append(ClaimStatus(name='Creada'))

        if not ClaimStatus.query.filter_by(name='En progreso').first():
            rows.append(ClaimStatus(name='En progreso'))

        if not ClaimStatus.query.filter_by(name='Aceptada').first():
            rows.append(ClaimStatus(name='Aceptada'))

        if not ClaimStatus.query.filter_by(name='Rechazada').first():
            rows.append(ClaimStatus(name='Rechazada'))

        if not ClaimStatus.query.filter_by(name='Postergada').first():
            rows.append(ClaimStatus(name='Postergada'))

        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def init_type_claims(self):
        rows = []
        if not ClaimType.query.filter_by(name='Sugerencia').first():
            rows.append(ClaimType(name='Sugerencia'))

        if not ClaimType.query.filter_by(name='Queja').first():
            rows.append(ClaimType(name='Queja'))

        if not ClaimType.query.filter_by(name='Solicitud').first():
            rows.append(ClaimType(name='Solicitud'))

        try:
            db.session.bulk_save_objects(rows)
            # db.session.add(claim_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
