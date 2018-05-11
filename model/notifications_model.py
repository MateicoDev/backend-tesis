from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from database import db
import datetime


class Notification(db.Model):
    __tablename__ = 'notifications'
    id_notification = db.Column(Integer, primary_key=True)
    notification_title = db.Column(String(100), nullable=False)
    notification_body = db.Column(String(300), nullable=False)
    read = db.Column(Boolean, nullable=False, default=False)
    visible = db.Column(Boolean, default=True, nullable=False)
    notification_datetime = db.Column(DateTime, nullable=False)
    id_notification_type = db.Column(Integer, ForeignKey('notification_types.id_notification_type'))
    notification_type = db.relationship('NotificationType', foreign_keys=[id_notification_type], cascade="merge")
    id_user = db.Column(Integer, ForeignKey('users.id_user'))
    user = db.relationship('User', foreign_keys=[id_user], cascade="merge")
    notification_picture = db.Column(String(300), nullable=True)


class NotificationType(db.Model):
    __tablename__ = 'notification_types'
    id_notification_type = db.Column(Integer, primary_key=True)
    notification_type_description = db.Column(String(100), nullable=False)
