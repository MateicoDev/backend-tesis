# -*- coding: utf8 -*-
import os
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")
ID_NOTIFICATION_TYPE_OTHERS = 1
# Cloud Messaging
# VECINDAPP_FIREBASE_API_KEY = "AAAAkprFulg:APA91bEsxzXJNSLMsccpO8Cq6eFRHzNijquDp1zMiNSWCE3wR2QxLbexMKxtIfbfZscZc" \
#                              "OCL_s1T0W" \
#                              "mxKZtaICpTKPgisxrDvp8AFV4o485k_9c81HqDfy7SjRmyTv-dRjbqFkqOVAvp"

#Claim
ID_NOTIFICATION_TYPE_CLAIM = 2
NOTIFICATION_TITLE_CLAIM = "Te han realizado un reclamo"
NOTIFICATION_BODY_CLAIM = "{} te ha realizado el reclamo"
CLAIM = "claim"

#Claim message
ID_NOTIFICATION_TYPE_CLAIM_MESSAGE = 3
NOTIFICATION_TITLE_CLAIM_MESSAGE = "Te han realizado un reclamo"
NOTIFICATION_BODY_CLAIM_MESSAGE = "{} te ha realizado el reclamo"
CLAIM_MESSAGE = "claim_message"