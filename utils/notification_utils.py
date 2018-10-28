from pyfcm import FCMNotification
from utils.settings import DBSettings
from model import Device, Notification
from database import db
from utils.constants import ID_NOTIFICATION_TYPE_OTHERS
import datetime


def send_notification(users, notification_title="Desconocido", notification_body="Desconocido",
                      id_notification_type=ID_NOTIFICATION_TYPE_OTHERS,
                      notification_picture="Desconocido", read=False, visible=True, notification_type=None):
    push_notification_service = FCMNotification(api_key=DBSettings.FIREBASE_API_KEY)
    notifications = []
    for id_user in users:
        notification = Notification(notification_title=notification_title, notification_body=notification_body,
                                    read=read, visible=visible, notification_datetime=datetime.datetime.now(),
                                    id_notification_type=id_notification_type, id_user=id_user,
                                    notification_picture=notification_picture)
        notifications.append(notification)
    try:
        db.session.add_all(notifications)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    devices = Device.query.filter(Device.id_user.in_(users)).all()
    if len(devices) > 0:
        data_message = {
            "notification_type": notification_type
        }
        registration_ids = [device.registration_id for device in devices]
        push_notification_service.notify_multiple_devices(registration_ids=registration_ids,
                                                          message_title=notification_title,
                                                          message_body=notification_body,
                                                          extra_kwargs={"id_notification_type": id_notification_type},
                                                          click_action="FCM_PLUGIN_ACTIVITY",
                                                          data_message=data_message)


# from pyfcm import FCMNotification
api_key="AAAA9D-eCTQ:APA91bEMC9JRBAfymOc3qbQ8tRwTdbJJEydsGlkJ0jYRZ14SUM0cdNxBIB2axPgb4hhXh-s9wNtcml_uTgM-FL-lhIHnZb9FFDxuypQuKvAkgaxTE1Zs42yCy9N0uN4CfxFjVr4s1DWP"
push_service = FCMNotification(api_key=api_key)
registration_id = api_key
message_title = "Hello World"
message_body = "My First PushNotification"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
print result