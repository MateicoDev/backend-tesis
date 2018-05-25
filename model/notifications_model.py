from database import db


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    visible = db.Column(db.Boolean, default=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    id_type = db.Column(db.Integer, db.ForeignKey('notification_types.id'))
    notification_type = db.relationship('NotificationType', foreign_keys=[id_type], cascade="merge")
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[id_user], cascade="merge")
    picture = db.Column(db.String(300), nullable=True)


class NotificationType(db.Model):
    __tablename__ = 'notification_types'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
