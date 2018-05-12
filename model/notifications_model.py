from database import db


class Notification(db.Model):
    __tablename__ = 'notifications'
    id_notification = db.Column(db.Integer, primary_key=True)
    notification_title = db.Column(db.String(100), nullable=False)
    notification_body = db.Column(db.String(300), nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    visible = db.Column(db.Boolean, default=True, nullable=False)
    notification_datetime = db.Column(db.DateTime, nullable=False)
    id_notification_type = db.Column(db.Integer, db.ForeignKey('notification_types.id_notification_type'))
    notification_type = db.relationship('NotificationType', foreign_keys=[id_notification_type], cascade="merge")
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    user = db.relationship('User', foreign_keys=[id_user], cascade="merge")
    notification_picture = db.Column(db.String(300), nullable=True)


class NotificationType(db.Model):
    __tablename__ = 'notification_types'
    id_notification_type = db.Column(db.Integer, primary_key=True)
    notification_type_description = db.Column(db.String(100), nullable=False)
