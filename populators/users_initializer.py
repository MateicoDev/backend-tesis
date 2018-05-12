from model import User
from database import db
from datetime import datetime

class UsersInitializer():
    def init_users(self):
        rows = []
        if not User.query.first():
            user_hired_date = datetime.now()
            rows.append(User(user_username='rovalle', user_password="mate123", user_name="Rodrigo",
                             user_lastname="Ovalle", user_email="r.ovalle@outlook.com",
                             user_profile_pic="FOTO", user_birth_date=user_hired_date,
                             user_sex="M", user_dni="38506000", user_phone="3515056824"))
            rows.append(User(user_username='santiinno', user_password="mate123", user_name="Santiago",
                             user_lastname="Innocenti", user_email="santi.innocenti@hotmail.com",
                             user_profile_pic="FOTO", user_birth_date=user_hired_date,
                             user_sex="M", user_dni="37732475", user_phone="3515215562"))
            rows.append(User(user_username='guadalupevocos', user_password="mate123", user_name="Guadalupe",
                             user_lastname="Vocos", user_email="vocosguadalupe@gmail.com",
                             user_profile_pic="FOTO", user_birth_date=user_hired_date,
                             user_sex="F", user_dni="37854262", user_phone="3513147750"))
            rows.append(User(user_username='juan.diaz', user_password="mate123", user_name="Juan",
                             user_lastname="Diaz", user_email="juan.diaz.cruz11@gmail.com",
                             user_profile_pic="FOTO", user_birth_date=user_hired_date,
                             user_sex="M", user_dni="38332661", user_phone="3515056824"))
        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
