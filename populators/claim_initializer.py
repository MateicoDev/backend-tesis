from model import ClaimType, ClaimStatus
from database import db


class ClaimInitializer():
    def init_status_claims(self):
        rows = []
        if not ClaimStatus.query.filter(ClaimStatus.name =='CREADA').first():
            rows.append(ClaimStatus(name='CREADA'))
        # if not ClaimStatus.query.filter_by(ClaimStatus.name == 'PENDIENTE').first():
        #     rows.append(ClaimStatus(name='PENDIENTE'))
        #
        # if not ClaimStatus.query.filter_by(ClaimStatus.name == 'FINALIZADA').first():
        #     rows.append(ClaimStatus(name='FINALIZADA'))

        try:

            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def init_type_claims(self):
        rows = []
        if not ClaimType.query.filter(ClaimType.name.in_('Reclamo')).first():
            claim_obj = ClaimType()
            claim_obj.name = 'Reclamo'
            # rows.append(ClaimType(name='Reclamo'))

        # if not ClaimType.filter(ClaimType.name.in_('General')).first():
        #     rows.append(ClaimType(name='General'))

        try:
            # db.session.bulk_save_objects(rows)
            db.session.add(claim_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
