# coding=utf-8


class NotificationServiceException(Exception):
    pass


class NotificationService(object):
    """
    Public Business Service


    Request
    =======
    GET /notifications

    lang: String. ISO 639-1 code. e.g: "es", "en", "pt".
    user_id: String. e.g: "CKJG3L".
    client_id: String. This id/code is unique for each registered client. e.g: "iphone_core_client".
    client_version: String. major.minor.stage.build  http://en.wikipedia.org/wiki/Software_versioning#Designating_development_stage  e.g: 1.4.3.25.
    client_tree_version: String. Tree version used by the client.
    client_api_version: String. REST API version used by the client.

    Response
    ========
    The response is a JSON notifications list  [{}]

    Notification fields:
    --------------------
    type: String. Required. Current valid options: "system", "user".
    code: String. Required. Current valid options: "sys_update", "usr_msg", "usr_confirm".
    mandatory: Boolean. Required. If true, client blocks until user take action. If false user can skip it.
    message: String. Required. Localized notificacion human readable message. Language is determined by lang request param.
    params: Object (dictionary). Optional. Notificacion parameters. Parameters are different for each notification type/code.

    TODO analyse:
    notificaction id/pk to check consumed notifications


    Samples:
    --------
    [
     {type: "system", code: "sys_update", mandatory: true, message: "Required application update", params: {url: "http://"}},
     {type: "user", code: "usr_msg", mandatory: false, message: "Hey buddy!, long time without logging food, are you still alive ?"}
    ]

    [
     {type: "system", code: "sys_update", mandatory: false, message: "Recommended application update", params: {url: "http://"}},
     {type: "user", code: "usr_msg", mandatory: false, message: "Your excercise budget for today is ****"
    ]

    """

    _logger = None

    def __init__(self, logger):
        self._logger = logger

    def get_notifications(self, client_id, client_version, client_tree_version, client_api_version, lang='en', user_id=None):
        notifications = []
        return notifications

    def get_update_notification(self):
        notifications = [{"id": 1, "type": "system", "code": "sys_update", "mandatory": True, "message": "Recommended application update", "params": {"url": "http://itunes.apple.com/ca/app/wikilife/id443072007?mt=8"}}]
        return notifications
