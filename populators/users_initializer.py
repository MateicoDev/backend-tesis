from model import User
from database import db
from datetime import datetime

class UsersInitializer():
    def init_users(self):
        rows = []
        if not User.query.first():
            user_hired_date = datetime.now()
            rows.append(User(user_username='rovalle', user_password="dinocloud123$", user_name="Rodrigo",
                             user_lastname="Ovalle", user_email="r.ovalle@outlook.com",
                             user_profile_pic="FOTO", user_birth_date=user_hired_date,
                             user_sex="M", user_dni="38506000", user_phone="3515056824"))
        try:
            db.session.bulk_save_objects(rows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
