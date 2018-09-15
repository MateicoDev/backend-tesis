from model import User
from database import db
from datetime import datetime

class UsersInitializer():
    def init_users(self):
        rows = []
        if not User.query.first():
            hired_date = datetime.now()
            rows.append(User(username='rovalle', password="fe5fa0e5941ac9ec4e1a0a07cdb4331a", name="Rodrigo",
                             lastname="Ovalle", email="r.ovalle@outlook.com",
                             profile_pic="FOTO", birth_date=hired_date,
                             sex="M", dni="38506000", phone="3515056824"))
            rows.append(User(username='santiinno', password="fe5fa0e5941ac9ec4e1a0a07cdb4331a", name="Santiago",
                             lastname="Innocenti", email="santi.innocenti@hotmail.com",
                             profile_pic="FOTO", birth_date=hired_date,
                             sex="M", dni="37732475", phone="3515215562"))
            rows.append(User(username='guadalupevocos', password="mate123", name="Guadalupe",
                             lastname="Vocos", email="vocosguadalupe@gmail.com",
                             profile_pic="FOTO", birth_date=hired_date,
                             sex="F", dni="37854262", phone="3513147750"))
            rows.append(User(username='juan.diaz', password="fe5fa0e5941ac9ec4e1a0a07cdb4331a", name="Juan",
                             lastname="Diaz", email="juan.diaz.cruz11@gmail.com",
                             profile_pic="FOTO", birth_date=hired_date,
                             sex="M", dni="38332661", phone="3515056824"))
            rows.append(User(username='administracion', password="fe5fa0e5941ac9ec4e1a0a07cdb4331a", name="Jorge",
                             lastname="Martinez", email="jmartinez@vecindapp.com",
                             profile_pic="FOTO", birth_date=hired_date,
                             sex="M", dni="23456789", phone="3515229090"))

        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
